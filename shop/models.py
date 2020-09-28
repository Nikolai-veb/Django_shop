from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import datetime
from PIL import Image
from django.utils.text import slugify




class Category(models.Model):
    """Категории"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
         return reverse('product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар"""

    category = models.ForeignKey(Category, verbose_name="Катеория", on_delete=models.CASCADE, related_name="products")
    name = models.CharField("Название товара", max_length=150)
    poster = models.ImageField("Изображение", upload_to="posters/", blank=True, null=True)
    slug = models.SlugField(max_length=300, unique=True)
    discription = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Склад", default=0)
    draft = models.BooleanField("Модераця", default=False)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-create"]


    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug":self.slug, "id":self.id})

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    """Изобржение продукта"""
    name = models.CharField("Имя", max_length=150)
    images = models.ImageField("Изобраение", upload_to="product_images/", null=True, blank=True)
    slug = models.SlugField(max_length=150, unique=True)
    product = models.ForeignKey(Product, verbose_name="Товар", related_name="product_images", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Изображение Товара"
        verbose_name_plural = "Изображение Товаров"

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


# class AbstractFavorit(models.Model):
#         class Meta:
#             abstract = True
#
#         user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
#
#         def __str__(self):
#             return self.user.username
#
# class BookmarkProduct(AbstractFavorit):
#         class Meta:
#             db_table = "bookmark_product"
#
#         obj = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)
#
# class BookmarkReview(AbstractFavorit):
#         class Meta:
#             db_table = "bookmark_review"
#
#         obj = models.ForeignKey(Review, verbose_name="Комментарий", on_delete=models.CASCADE)


