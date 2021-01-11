from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from django.urls import reverse
from django.utils.safestring import mark_safe


class CustomUser(AbstractUser):
    """Customer Model User"""
    avatar = models.ImageField("Аватарка", upload_to="account/avatar/", null=True, blank=True)
    date_birth = models.DateField("Дата рождения", null=True, blank=True)

    def get_absolute_url(self):
        return reverse('custom_users', kwargs={"pk": self.id})

    def get_image(self):
        """The function of displaying pictures in the admin panel"""
        if self.avatar:
            return mark_safe(f'<img src={self.avatar.url} width="50" height="60">')
        else:
            return '(Нет изображения)'
    get_image.short_description = "Аватарка"
    get_image.allow_tags = True


