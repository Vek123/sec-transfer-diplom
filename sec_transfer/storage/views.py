__all__ = ()

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.utils import safe_order_by
from storage.forms import FileCreateForm
from storage.models import File


class FileCatalogView(LoginRequiredMixin, ListView):
    template_name = 'storage/catalog.html'
    context_object_name = 'files'

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
        return super().form_valid(form)


class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = File
    success_url = reverse_lazy('storage:catalog')
    template_name = 'storage/delete_file.html'


class FileUpdateView(LoginRequiredMixin, UpdateView):
    model = File
    template_name = 'storage/update_file.html'
    form_class = FileCreateForm

    def get_success_url(self):
        return reverse('storage:update', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, _('File was successfully updated'))
        return super().form_valid(form)
