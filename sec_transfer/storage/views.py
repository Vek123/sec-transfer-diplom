__all__ = ()

import base64

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from core.utils import safe_order_by
from crypto.utils import get_private_key, RSA_ENCRYPT_PADDING, sign_aes_key
from storage.forms import FileCreateForm
from storage.models import File

CATALOG_FILES_PER_PAGE = 10


class FileCatalogView(LoginRequiredMixin, ListView):
    template_name = 'storage/catalog.html'
    context_object_name = 'files'
    paginate_by = CATALOG_FILES_PER_PAGE

    def get_queryset(self):
        query = File.owned.catalog(self.request.user)
        sorted_by_field = self.request.GET.get('sorted_by_field', '')
        query = safe_order_by(
            query,
            sorted_by_field,
            [File.file.field.name],
        )

        return query


class FileCreateView(LoginRequiredMixin, CreateView):
    model = File
    template_name = 'storage/create_file.html'
    form_class = FileCreateForm
    success_url = reverse_lazy('storage:catalog')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, _('File was successfully created'))
        return super().form_valid(form)


class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = File
    success_url = reverse_lazy('storage:catalog')
    template_name = 'storage/delete_file.html'

    def form_valid(self, form):
        messages.success(self.request, _('File was successfully deleted'))
        return super().form_valid(form)


class FileUpdateView(LoginRequiredMixin, UpdateView):
    model = File
    template_name = 'storage/update_file.html'
    form_class = FileCreateForm

    def get_success_url(self):
        return reverse('storage:update', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, _('File was successfully updated'))
        return super().form_valid(form)


class FileCryptoDataView(LoginRequiredMixin, SingleObjectMixin, View):
    queryset = File.objects.values(
        File.iv.field.name,
        File.encrypted_key.field.name,
        File.gcm_tag.field.name,
    )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        aes_key = base64.b64decode(self.object[File.encrypted_key.field.name])
        with get_private_key() as private_key:
            aes_key = private_key.decrypt(aes_key, RSA_ENCRYPT_PADDING)

        aes_key_sign = sign_aes_key(aes_key)
        self.object[File.encrypted_key.field.name] = (
            base64.b64encode(aes_key).decode()
        )
        self.object['aes_key_sign'] = (
            base64.b64encode(aes_key_sign).decode()
        )

        return JsonResponse(self.object)
