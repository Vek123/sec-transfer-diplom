__all__ = ()

from django.db import models

from storage.querysets import FileQuerySet


class FileManager(models.Manager.from_queryset(FileQuerySet)):
    def catalog(self):
        queryset = self.get_queryset()
        return queryset.with_user().default_only()


class OwnedFileManager(FileManager):
    def catalog(self, user):
        query = super().catalog()
        return query.filter(user=user)
