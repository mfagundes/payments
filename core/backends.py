from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    Using a different AUTHENTICATION BACKEND to keep compatibility with the cookiecutter,
    but the best option would be creating a custom user. This is a very simple solution,
    once it demands that both username and email are the same
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
