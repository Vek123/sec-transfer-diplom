__all__ = ()

from django import forms

from core.forms import BootrapFormMixin
from storage.models import File


class FileCreateForm(BootrapFormMixin, forms.ModelForm):
    class Meta:
        model = File
        fields = (
            File.file.field.name,
            File.iv.field.name,
            File.gcm_tag.field.name,
            File.encrypted_key.field.name,
        )
        widgets = {
            File.iv.field.name: forms.HiddenInput(),
            File.gcm_tag.field.name: forms.HiddenInput(),
            File.encrypted_key.field.name: forms.HiddenInput(),
        }
