from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib import admin



class UserNetAdmin(UserAdmin):
    """Setting User Model """
    list_display = ('username', 'email', "avatar", "get_image")
    save_on_top = True
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Personal info'), {'fields': ('avatar', 'date_birth')}),
    )



admin.site.register(CustomUser, UserNetAdmin)

