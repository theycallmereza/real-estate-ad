from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('phone_number', 'is_staff', 'is_active', 'phone_number_verified')
    list_filter = ('phone_number', 'is_staff', 'is_active', 'phone_number_verified')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password', 'phone_number_verified')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_active', 'phone_number_verified')
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
