from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from couponss.models import Coupon


class Order(models.Model):
    """Заказ"""
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамлия", max_length=50)
    email = models.EmailField("Email")
    city = models.CharField("Город проживания", max_length=50)
    address = models.CharField("Адрес доставки", max_length=250)
    postal_code = models.CharField("Почтовый индекс", max_length=20)
    pained = models.BooleanField("Оплаченно", default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon, verbose_name="Купон", null=True, blank=True, related_name="orders", on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created"]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.item.all())
        return total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    """Наменклатура заказа"""
    order = models.ForeignKey(Order, verbose_name="Заказ", related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Товар", related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=0)

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.price * self.quantity
