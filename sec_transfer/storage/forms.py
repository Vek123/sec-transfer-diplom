__all__ = ()

from django import forms

from core.forms import BootrapFormMixin
from storage.models import File


class FileCreateForm(BootrapFormMixin, forms.ModelForm):
    class Meta:
        model = File
        fields = (File.file.field.name,)
