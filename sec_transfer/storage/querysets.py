__all__ = ()

from django.db import models


class FileQuerySet(models.QuerySet):
    def with_user(self):
        from storage.models import File

        return self.select_related(
            File.user.field.name,
        )

    def default_only(self, *extra):
        from storage.models import File
        from users.models import User

        return self.only(
            *extra,
            File.file.field.name,
            File.created_at.field.name,
            File.updated_at.field.name,
            f'{File.user.field.name}__{User.first_name.field.name}',
            f'{File.user.field.name}__{User.last_name.field.name}',
            f'{File.user.field.name}__{User.patronymic.field.name}',
        )
