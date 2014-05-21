from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from auth.forms import AdminUserCreationForm

class BaseUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'user_type', 'email', 'password1', 'password2')}
        ),
    )
    add_form = AdminUserCreationForm
        
admin.site.unregister(User)
admin.site.register(User, BaseUserAdmin)
