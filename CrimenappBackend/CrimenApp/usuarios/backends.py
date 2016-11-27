

from django.conf import settings
from django.contrib.auth.hashers import check_password
from usuarios.models import MyUser as User
from django.contrib.auth.backends import ModelBackend


# class CustomBackend(ModelBackend):

    # def authenticate(self, username=None, password=None):
    #     login_valid = (settings.ADMIN_LOGIN == username)
    #     pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
    #     if login_valid and pwd_valid:
    #         try:
    #             user = User.objects.get(username=username)
    #         except User.DoesNotExist:
    #             # Create a new user. There's no need to set a password
    #             # because only the password from settings.py is checked.
    #             user = User(username=username)
    #             user.is_staff = True
    #             user.is_superuser = True
    #             user.save()
    #         return user
    #     return None

    # def get_user(self, user_id):
    #     try:
    #         return User.objects.get(pk=user_id)
    #     except User.DoesNotExist:
    #         return None