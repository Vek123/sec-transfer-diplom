__all__ = ()

from django.contrib import admin

from storage import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    fields = (
        models.File.file.field.name,
        models.File.user.field.name,
        models.File.created_at.field.name,
        models.File.updated_at.field.name,
        models.File.encrypted_key.field.name,
    )
    readonly_fields = (
        models.File.created_at.field.name,
        models.File.updated_at.field.name,
    )
    list_display = (
        models.File.file.field.name,
        models.File.user.field.name,
        models.File.created_at.field.name,
        models.File.updated_at.field.name,
    )
    list_display_links = (models.File.file.field.name,)
