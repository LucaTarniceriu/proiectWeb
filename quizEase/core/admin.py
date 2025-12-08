from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Quiz, Question, Submits

class CustomUserAdmin(UserAdmin):
    # Add your custom field to the fieldsets (for editing a user)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('isProfesor',)}),
        (None, {'fields': ('activeQuiz',)}),
    )

    # Add your custom field to the add_fieldsets (for creating a user)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('isProfesor',)}),
        (None, {'fields': ('activeQuiz',)}),
    )

    # Optional: show it in the list display
    list_display = UserAdmin.list_display + ('isProfesor', 'activeQuiz')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Submits)