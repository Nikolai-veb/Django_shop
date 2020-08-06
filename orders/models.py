from django.db import models
from shop.models import Product


class Order(models.Model):
    """Заказ"""
    first_name = models.CharField("Имя", max_lenth=50)
    last_name = models.CharField("Фамлия", max_lenth=50)
    email = models.EmailField("Email")
    city = models.CharField("Город проживания", max_lenth=50)
    adress = models.CharField("Адрес доставки", max_lenth=250)
    postal_code = models.CharField("Почтовый индекс", max_lenth=20)
    paind = models.BooleanField("Оплаченно", default=False)
    created = models.DateTimeField(auto_add_now=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created"]

    def __str__(self):
        return 'Order %s '%(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Наменклатура заказа"""
    order = models.ForeignKey(Order, verbose_name="Заказ", related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Товар", related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", defalt=0)

    def __str__(self):
        return "{}".format(self.id)

    def get_cost(self):
        return self.price * self.quantity
