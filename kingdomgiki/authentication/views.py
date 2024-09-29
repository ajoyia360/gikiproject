from django.shortcuts import render

# Create your views here.
from django.core.mail import send_mail
from django.conf import settings

# function of app
from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.models import UserModel
# authentication/views.py

from django.shortcuts import render

def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",  # Add any other variables you want to pass
    })
    return context


def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        user = UserModel.objects.get(email=request.user.email)  # Get the user

        if code == user.verification_code:
            user.is_verified = True  # Update the user's verification status
            user.save()
            messages.success(request, 'Your email has been verified successfully!')
            return redirect('#')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid verification code.')

    return render(request, 'authentication/verify_email.html')  # Render your verification template


def send_mail_to():
    print("From Email:", settings.DEFAULT_FROM_EMAIL)
    print("To Email:", ['ahsanasif759759@gmail.com'])

    send_mail(
        subject='Test Email',  # Subject of the email
        message='This is a test email to verify the setup.',  # Email body
        from_email=settings.DEFAULT_FROM_EMAIL,  # Sender's email
        recipient_list=['ahsanasif759759@gmail.com'],  # Replace with recipient's email
        fail_silently=False,  # Set to True to suppress errors
    )
