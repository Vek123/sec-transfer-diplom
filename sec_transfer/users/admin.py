__all__ = ()

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


class UserAdmin(BaseUserAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.fieldsets[1][1]['fields'] = (
            User.first_name.field.name,
            User.last_name.field.name,
            User.patronymic.field.name,
        )


admin.site.register(User, UserAdmin)
