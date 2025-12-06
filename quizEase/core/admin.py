from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Add your custom field to the fieldsets (for editing a user)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('isProfesor',)}),
    )

    # Add your custom field to the add_fieldsets (for creating a user)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('isProfesor',)}),
    )

    # Optional: show it in the list display
    list_display = UserAdmin.list_display + ('isProfesor',)

admin.site.register(User, CustomUserAdmin)