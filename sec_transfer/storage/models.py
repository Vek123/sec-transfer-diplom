__all__ = ()

from django.db import models
from django.utils.translation import gettext_lazy as _

from storage.apps import StorageConfig
from storage.managers import FileManager, OwnedFileManager
from users.models import User


class File(models.Model):
    objects = FileManager()
    owned = OwnedFileManager()

    def _upload_to(self, filename):
        return f'{StorageConfig.name}/{self.user.username}/{filename}'

    file = models.FileField(
        _('file'),
        upload_to=_upload_to,
    )
    encrypted_key = models.CharField(
        _('encrypted key'),
        max_length=32,
        help_text=_('Max length 32'),
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='files',
        related_query_name='files',
    )
