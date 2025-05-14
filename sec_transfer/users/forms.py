__all__ = ()

from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _

from core.forms import BootrapFormMixin
from users.models import User


class SignUpForm(BootrapFormMixin, auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = _(
            'Минимум 8 символов',
        )
        self.fields['password2'].widget.attrs['placeholder'] = _(
            'Повторите пароль',
        )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
        )
        labels = {
            User.username.field.name: _('Логин'),
            User.email.field.name: _('Адрес электронной почты'),
        }
        help_texts = {
            User.username.field.name: _('Максимум 150 символов'),
            User.email.field.name: _('Максимум 254 символа'),
        }


class LoginForm(BootrapFormMixin, auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(
        label=_('Логин или почта'),
        widget=forms.TextInput(attrs={'autofocus': True}),
    )


class PasswordChangeForm(BootrapFormMixin, auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['placeholder'] = _(
            'Введите пароль длиной от 8 символов',
        )
        self.fields['old_password'].widget.attrs['placeholder'] = _(
            'Введите пароль длиной от 8 символов',
        )


class PasswordResetForm(BootrapFormMixin, auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label=_('Введите почту, привязанную к аккаунту'),
        help_text=_('Максимум 254 символа'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )


class PasswordResetConfirmForm(BootrapFormMixin, auth_forms.SetPasswordForm):
    pass


class ProfileForm(BootrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = (
            User.first_name.field.name,
            User.last_name.field.name,
            User.patronymic.field.name,
        )
        labels = {
            User.first_name.field.name: _('Имя'),
            User.last_name.field.name: _('Фамилия'),
            User.patronymic.field.name: _('Отчество (при наличии)'),
        }
