from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import CustomUser

class PhoneNumberAuthBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            # Найти пользователя по номеру телефона
            user = CustomUser.objects.get(phone_number=phone_number)
            # Проверить пароль
            if check_password(password, user.password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
