__all__ = ()

from django.views.generic import ListView

from core.utils import safe_order_by
from storage.models import File


class FileCatalogView(ListView):
    queryset = File.objects.catalog()
    template_name = 'storage/catalog.html'
    context_object_name = 'files'

    def get_queryset(self):
        query = super().get_queryset()
        sorted_by_field = self.request.GET.get('sorted_by_field', '')
        query = safe_order_by(
            query,
            sorted_by_field,
            [File.file.field.name],
        )

        return query
