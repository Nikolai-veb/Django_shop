from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nikname', 'photo', 'date_birth')
    list_filter = ('nikname', 'date_birth')
    search_fields = ('nikname', 'date_birth')
