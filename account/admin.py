from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'photo', 'date_birth')
    list_filter = ('username', 'date_birth')
    search_fields = ('username', 'date_birth')
