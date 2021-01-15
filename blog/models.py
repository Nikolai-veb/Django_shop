from django.db import models
from account.models import CustomUser
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify


class Tag(models.Model):
    """Таг"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("article_list_by_tag", kwargs={"tag_slug": self.slug})

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Article(models.Model):
    """Модель статьи"""
    user = models.ForeignKey(CustomUser, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="articles")
    title = models.CharField("Заголовок", max_length=500)
    tags = models.ManyToManyField(Tag, verbose_name="Тэги", related_name="articles")
    image = models.ImageField("Изображение", upload_to="image_blog/", blank=True, null=True)
    body = models.TextField("Текст", blank=True, null=True)
    draft = models.BooleanField("Черновик", default=False)
    slug = models.SlugField(max_length=1000, unique=True, db_index=True)
    create = models.DateTimeField("Дата создания", auto_now_add=True)
    update = models.DateTimeField("Дата обнавления", auto_now=True)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={"pk": self.id})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-create']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, self.create)
        super(Article, self).save(*args, **kwargs)


class Comment(models.Model):
    """Комментарии"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=1000)
    text = models.TextField("Текст", max_length=50000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Article, verbose_name="Статья", on_delete=models.CASCADE, related_name="reviews")
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'{self.name}-{self.article}'
