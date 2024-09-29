from django.contrib import admin
from .models import UserModel, StudentReview
from unfold.admin import ModelAdmin

@admin.register(UserModel)
class UserModelAdmin(ModelAdmin):
    list_display = ('username', 'email', 'student_id', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'student_id')

    class Media:
        css = {
            'all': ('authentication/css/custom_admin.css',)  # Custom CSS path
        }
        js = ('authentication/js/custom_admin.js',)  # Include custom JS if needed

@admin.register(StudentReview)
class StudentReviewAdmin(ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('status',)

    actions = ['approve_student', 'reject_student']

    def approve_student(self, request, queryset):
        for review in queryset:
            if review.status != 'Approved':  # Only approve pending users
                review.status = 'Approved'
                review.user.is_active = True  # Activate the user
                review.user.save()
                review.save()
        self.message_user(request, "Selected student reviews have been approved.")

    approve_student.short_description = "Approve selected student reviews"

    def reject_student(self, request, queryset):
        for review in queryset:
            if review.status != 'Rejected':  # Only reject pending users
                review.status = 'Rejected'
                review.user.is_active = False  # Deactivate the user
                review.user.save()
                review.save()
        self.message_user(request, "Selected student reviews have been rejected.")

    reject_student.short_description = "Reject selected student reviews"

    class Media:
        css = {
            'all': ('authentication/css/custom_admin.css',)  # Custom CSS path
        }
        js = ('authentication/js/custom_admin.js',)  # Include custom JS if needed
