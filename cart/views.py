from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    """Oбработчик для добавления товаров в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    """Обработчик для удаления товара из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    """Oбработчик для страницы списка товаров, добавленных в корзину"""
    cart = Cart(request)
    products = cart.list_items()
    for item in cart.inter():
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                    'update': True}
        )
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'products': products})


