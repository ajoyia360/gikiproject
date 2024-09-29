from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class CaseInsensitiveModelBackend(ModelBackend):
    # first it will check the username; if not provided, it sets the default as None; then it will take the email from kwargs which is a dictionary.
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            # email is stored inside the username.
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            # this is equal to Users.objects.get(uncaptured which email as string.)
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
