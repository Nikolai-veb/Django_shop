from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Coupon(models.Model):
    code = models.CharField("Коде", max_length=50, unique=True)
    coupon_start = models.DateTimeField("Начала действия купона")
    coupon_finish = models.DateTimeField("Истечение действия купона",)
    discount = models.IntegerField("Скидка", validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField("Активацыя", default=False)

    class Meta:
        verbose_name = "Купон"
        verbose_name_plural = "Купоны"

    def __str__(self):
        return self.code
