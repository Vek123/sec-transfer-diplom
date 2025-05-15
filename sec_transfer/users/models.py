__all__ = ()

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class User(AbstractUser):
    objects = UserManager()

    username = models.CharField(
        _('username'),
        max_length=32,
        unique=True,
        help_text=_(
            'Обязательно. 32 символа или меньше.'
            ' Только буквы, цифры и @/./+/-/_',
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _('Пользователь с таким именем уже существует.'),
        },
    )
    email = models.EmailField(
        _('email address'),
        max_length=256,
        unique=True,
        help_text=_('Должен соответствовать формату <АДРЕС>@<ДОМЕН>.<ЗОНА>'),
    )
    patronymic = models.CharField(
        _('patronymic'),
        max_length=150,
        blank=True,
    )

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return (
            f'{self.last_name}'
            f'{f" {self.first_name[0]}." if self.first_name else ""}'
            f'{f" {self.patronymic[0]}." if self.patronymic else ""}'
        )
