from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Favorites(object):
    def __init__(self, request):
        """Инициализация объекта корзины."""
        self.session = request.session
        favorite = self.session.get(settings.FAVORITE_SESSION_ID)
        if not favorite:
            # Сохраняем в сессии пустую корзину.
            favorite = self.session[settings.FAVORITE_SESSION_ID] = {}
        self.favorite = favorite

    def add(self, product):
        """Добавление товара в корзину или обновление его количества."""
        product_id = str(product.id)
        if product_id not in self.favorite:
            self.favorite[product_id] = {'quantity': 1, 'price': str(product.price)}
        # if update_quantity:
        # self.favorite[product_id]['quantity'] = quantity
        # else:
        #     self.favorite[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины."""
        product_id = str(product.id)
        if product_id in self.favorite:
            del self.favorite[product_id]
        self.save()

    def inter(self):
        """Проходим по товарам корзины и получаем соответствующие объекты Product."""
        product_ids = [i for i in self.favorite.keys()]
        # Получаем объекты модели Product и передаем их в корзину
        products = Product.objects.filter(id__in=product_ids)
        favorite = self.favorite.copy()
        favorites = []
        for product in products:
            favorite[str(product.id)]['product'] = product
        for item in favorite.values():
            item['price'] = Decimal(item['price'])
            #     item['total_price'] = item['price'] * item['quantity']
            favorites.append(item)
        return favorites

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.favorite.values())

    def clear(self):
        # Очистка корзины.
        del self.session[settings.FAVORITE_SESSION_ID]
        self.save()
