__all__ = ()

from django.contrib.auth.models import UserManager as BaseUserManager


class UserManager(BaseUserManager):
    def by_mail(self, email):
        return self.get(email=email)
