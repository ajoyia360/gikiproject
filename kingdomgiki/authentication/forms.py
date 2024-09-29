# friendsystem/forms.py

from django import forms
from authentication.models import UserModel


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = [
            'email',
            'username',
            'student_id',
            'profile_image',
            'date_of_birth',
            'faculty',
            'hostel',
            'room_number',
            'hobbies',
            'uni_id_card',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Hash the password
        if commit:
            user.save()
        return user
