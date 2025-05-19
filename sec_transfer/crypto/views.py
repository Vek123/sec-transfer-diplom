__all__ = ()

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from crypto.utils import set_public_key_header


class GetPublicKeyView(LoginRequiredMixin, View):
    def get(self, request):
        response = redirect(request.META.get('HTTP_REFERER'))
        response.headers['Set-Cookie'] = set_public_key_header()
        messages.success(request, _('Public key was successfully updated'))
        return response
