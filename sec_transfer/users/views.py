__all__ = ()

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, View

from users import forms
from users.models import User


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/profile.html'
    form_class = forms.ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.request.user
        kwargs.update(
            {'instance': instance},
        )

        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Изменения сохранены'))
        return super().form_valid(form)


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = forms.SignUpForm

    def form_valid(self, form):
        form.instance.is_active = False
        form.save()
        self.send_verification_email(form.instance)
        message = _(
            'Пожалуйста, перейдите по ссылке в письме, чтобы подвердить почту',
        )
        messages.success(self.request, _(message))
        return redirect('users:login')

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = settings.ORIGIN + reverse(
            'users:verify_email',
            args=[uid, token],
        )

        subject = _('Подтверждение регистрации')
        message = render_to_string(
            'users/confirmation_email_text.html',
            {
                'user_name': user.username,
                'confirmation_url': verification_link,
            },
        )

        html_message = render_to_string(
            'users/confirmation_email.html',
            {'confirmation_email_text': message},
        )

        user.email_user(
            subject,
            message,
            html_message=html_message,
        )


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save(update_fields=[User.is_active.field.name])
            messages.success(self.request, _('Почта успешно активирована'))
            return redirect('users:login')

        messages.error(self.request, _('Не удалось активировать почту'))
        return redirect('users:signup')
