from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from utils.admin import BaseAdmin, BaseInlineStackedAdmin
from core.models import Profile


class ProfileInline(BaseInlineStackedAdmin):
    """
    Class to create inline profile in admin
    """
    model = Profile
    can_delete = False
    verbose_name = 'perfil'
    verbose_name_plural = 'perfis'


# Define a new User admin
class UserAdmin(BaseAdmin):
    """
    Overwrite BaseAdmin to include profile inline
    """
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
