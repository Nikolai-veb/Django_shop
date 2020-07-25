from django.db import models
from django.urls import reverse
from datetime import date

class Category(models.Model):
    """Категории"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар"""
    category = models.ForeignKey(Category, verbose_name="Катеория", on_delete=models.CASCADE, related_name="products")
    name = models.CharField("Название товара", max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    images = models.ImageField("Изобраение", upload_to="product/", null=True, blank=True)
    discription = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Склад", default=0)
    draft = models.BooleanField("Модераця", default=False)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def get_absolute_url(self):
        return reverse("product_detail", kwards={"slug":self.slug})

    def __str__(self):
        return self.name


class RatingStar(models.Model):
    """Звезды рейтинга"""
    value = models.PositiveIntegerField("Звезды", default=0)

    class Meta:
        verbose_name = "Звезды рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ['-value']

    def __str__(self):
        return f'{self.value}'


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адресс", max_length=15)
    star = models.ForeignKey(RatingStar, verbose_name="Звезды", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE, related_name="ratings")

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинг"

    def __str__(self):
        return f'{self.star}-{self.product}'


class Review(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=1000)
    text =  models.TextField("Текст", max_length=50000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE, related_name="reviews")
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


    def __str__(self):
        return f'{self.name}-{self.product}'
