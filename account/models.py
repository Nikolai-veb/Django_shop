from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from PIL import Image


class Profile(models.Model):
    """Профиль"""
    username = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    date_birth = models.DateTimeField("Дата рождения", blank=True, null=True)
    photo = models.ImageField("Фото", upload_to='profile/%Y/%m/%d', null=True, blank=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f'Профиль пользователя  {self.username}'
