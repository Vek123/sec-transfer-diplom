__all__ = ()

import re

from django.contrib.auth.backends import ModelBackend

from users.models import User

EMAIL_REGEX = re.compile(r'.+@.+\..+')


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if EMAIL_REGEX.fullmatch(username) is None:
                return None

            email = User.objects.normalize_email(username)
            user = User.objects.by_mail(email)
            if not self.user_can_authenticate(user):
                return None

            if not user.check_password(password):
                return None

            return user
        except User.DoesNotExist:
            return None
