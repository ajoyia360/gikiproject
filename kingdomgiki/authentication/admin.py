from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from authentication.models import StudentReview, UserModel

class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'student_id', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email', 'student_id')
    ordering = ('username',)

    class Media:
        css = {
            'all': ('authentication/css/custom_admin.css',)  # Your custom CSS path
        }
        js = ('friendsystem/js/custom_admin.js',)  # Include custom JS if needed for additional interactivity

class StudentReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'user__email')

    actions = ['approve_student', 'reject_student']

    def approve_student(self, request, queryset):
        """Approve selected users and activate their accounts."""
        approved_users = []
        for review in queryset:
            if review.status != 'Approved':  # Only approve pending users
                review.status = 'Approved'
                review.user.is_active = True  # Activate the user
                review.user.save()
                review.save()
                approved_users.append(review.user.email)  # Collect approved user emails
                review.send_email_notification()  # Notify user

        self.message_user(request, f"{len(approved_users)} students approved and notified.")  # Success message

    approve_student.short_description = "Approve selected students"

    def reject_student(self, request, queryset):
        """Reject selected users and deactivate their accounts."""
        rejected_users = []
        for review in queryset:
            if review.status != 'Rejected':  # Only reject pending users
                review.status = 'Rejected'
                review.user.is_active = False  # Deactivate the user
                review.user.save()
                review.save()
                rejected_users.append(review.user.email)  # Collect rejected user emails
                review.send_email_notification()  # Notify user

        self.message_user(request, f"{len(rejected_users)} students rejected and notified.")  # Success message

    reject_student.short_description = "Reject selected students"

    class Media:
        css = {
            'all': ('friendsystem/css/custom_admin.css',)  # Your custom CSS path
        }
        js = ('friendsystem/js/custom_admin.js',)  # Add custom JS if needed

# Register your models and custom admin classes
admin.site.register(UserModel, UserModelAdmin)
admin.site.register(StudentReview, StudentReviewAdmin)
