from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.options import BaseModelAdmin

from utils.admin import BaseAdmin, BaseInlineStackedAdmin
from core.models import Profile, Payment, PaymentAdvance


class ProfileInline(BaseInlineStackedAdmin):
    """
    Class to create inline profile in admin
    """
    model = Profile
    can_delete = False
    verbose_name = 'perfil'
    verbose_name_plural = 'perfis'


class PaymentAdvanceInlineAdmin(BaseInlineStackedAdmin):
    model = PaymentAdvance
    readonly_fields = ('payment', 'original_value', 'original_due_date', 'new_value', 'requested_by')
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    """
    Overwrite BaseAdmin to include profile inline
    """
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff',)
    search_fields = ('profile__company_name', )


@admin.register(Payment)
class PaymentAdmin(BaseAdmin):
    """
    Admin for payments, to allow company operators to add and change
    """
    inlines = (PaymentAdvanceInlineAdmin, )
    list_display = ('provider', 'due_date', 'value')
    ordering = ('due_date',)
    autocomplete_fields = ('provider',)
    list_filter = ('provider__profile__company_name',)


@admin.register(PaymentAdvance)
class PaymentAdvanceAdmin(BaseAdmin):
    """
    To provide operators the capacity to request an advance in a payment
    coming through other sources, instead of the API endpoints
    """
    readonly_fields = ('original_due_date', 'original_value', 'new_value', 'requested_by')

    def save_model(self, request, obj, form, change):
        obj.requested_by = request.user
        obj.save()


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
