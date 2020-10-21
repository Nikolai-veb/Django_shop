from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Article(models.Model):
    """Модель статьи"""
    user = models.ForeignKey(User, verbose_name="", on_delete=models.CASCADE, related_name="articles")
    title = models.CharField("Заголовок", max_length=500)
    image = models.ImageField("Изображение", upload_to="image_blog/", blank=True, null=True)
    body = models.TextField("Текст")
    draft = models.BooleanField("Черновик", default=False)
    slug = models.SlugField(max_length=1000, unique=True, db_index=True)
    create = models.DateTimeField("Дата создания", auto_now_add=True)
    update = models.DateTimeField("Дата обнавления", auto_now=True)

    def get_asolute_url(self):
        return reverce('article_detail', kwargs={"pk": self.id}) 

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-create']


