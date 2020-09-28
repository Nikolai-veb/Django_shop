from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, Rating, RatingStar, Review, ProductImages
from PIL import Image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_dislay = ("name", "slug")
    list_filter = ("name",)
    searche_fields = ("name",)
    prepopulated_fields = {'slug': ('name',)}


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1
    readonly_fields = ("get_image",)

    # Функыця отоброжения картинок в админке
    def get_image(self, odj):
        return mark_safe(f'<img src={odj.images.url} widht="50" height="60">')

    get_image.short_description = "Изображение"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "slug",
        "draft",

    )

    list_filter = ("name", "price", "category")
    list_editable = ("draft",)
    search_fields = ("name", "price", "category")
    prepopulated_fields = {'slug': ('name', 'price')}
    inlines = [ProductImagesInline,]
    fieldsets = (
        (None,{
            "fields":(("name", "category"),)
        }),
        (None,{
            "fields":("discription",)
        }),
        (None,{
            "fields":("slug",)
        }),
        (None,{
            "fields":("poster",)
        }),
        (None,{
            "fields":(("price", "stock", "draft"))
        }),
       # (None,{
           # "fields":("create", "update")
       # })
    )


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product", "slug", "get_image")
    list_display_links =("name",)
    readonly_fields = ("get_image",)
    list_filter = ("name", "product")
    search_fields = ("name", "product")
    prepopulated_fields = {'slug': ('name', 'product')}



    def get_image(self, odj):
        """Функцыя показа изображения"""
        return mark_safe(f'<img src={odj.images.url} widht="100" height="110">')

    get_image.short_description = "Изображение"


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_dislay = ("id", "value")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_dislay = ("name", "email", "parent", "product", "create")
    list_filter = ("name", "email", "product", "create")
    searche_fields = ("name", "product")

