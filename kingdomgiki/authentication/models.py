from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom Manager for UserModel
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, student_id, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not student_id:
            raise ValueError('Users must have a student ID')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            student_id=student_id,
        )
        user.set_password(password)
        user.is_active = False  # User is inactive until approved
        user.save(using=self._db)

        # Create a student review for this user
        if not user.is_superuser:
            StudentReview.objects.create(user=user)

        return user

    def create_superuser(self, email, username, student_id, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            student_id=student_id
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  # Superusers are active immediately
        user.save(using=self._db)
        return user

# Custom User Model
class UserModel(AbstractBaseUser):
    student_id = models.CharField(
        max_length=7,
        primary_key=True,
        validators=[RegexValidator(
            regex=r'^\d{7}$',
            message="Student ID must be exactly 7 digits long."
        )],
        unique=True
    )
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(
        verbose_name="email",
        max_length=60,
        unique=True
    )
    profile_image = CloudinaryField('image', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    faculty_choices = [
        ('Civil Engineering', 'Civil Engineering'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('AI', 'AI'),
        ('Software Engineering', 'Software Engineering'),
        ('Computer Engineering', 'Computer Engineering'),
        ('Management Sciences', 'Management Sciences'),
        ('Computer Science', 'Computer Science')
    ]
    faculty = models.CharField(max_length=50, choices=faculty_choices, blank=True)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive')
    hostel_choices = [(str(i), f'Hostel {i}') for i in range(1, 13)]
    hostel = models.CharField(max_length=2, choices=hostel_choices)
    room_number = models.IntegerField(null=True, blank=True)
    hobbies = models.TextField(blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # Set default to False
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    account_created_at = models.DateTimeField(verbose_name='account created at', auto_now_add=True)
    account_updated_at = models.DateTimeField(verbose_name='account updated at', auto_now=True)
    uni_id_card = CloudinaryField('image', null=True, blank=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'student_id']

    def __str__(self):
        return f'{self.username} ({self.student_id})'

    def get_full_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def age(self):
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        if age < 16:
            raise ValueError("User must be at least 16 years old.")
        return age

# Model to handle student review process by admin
class StudentReview(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    review_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.user.username} - Status: {self.status}"

    def send_email_notification(self):
        """Send email notification to the user based on the review outcome."""
        subject = ''
        message = ''
        if self.status == 'Approved':
            subject = 'Registration Approved'
            message = f"Dear {self.user.username}, your registration has been approved. Welcome to Kingdom GIKI!"
        elif self.status == 'Rejected':
            subject = 'Registration Rejected'
            message = f"Dear {self.user.username}, unfortunately, your registration was rejected. Reason: {self.review_comment}."
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            fail_silently=False,
        )

# Signal to trigger when StudentReview is updated
@receiver(post_save, sender=StudentReview)
def review_status_change(sender, instance, **kwargs):
    """Send notification email to user when their review status changes."""
    # Check if the status has changed to either 'Approved' or 'Rejected'
    if instance.status in ['Approved', 'Rejected']:
        instance.send_email_notification()
