from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('display_name', 'bio', 'avatar')}),
    )
    list_display = ('username', 'email', 'display_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'display_name')
