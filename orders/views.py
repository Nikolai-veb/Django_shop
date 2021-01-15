from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCraeteForm
from cart.cart import Cart
from .tasks import send_spam_email


def order_create(request):
    """Обработчик заказов"""
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCraeteForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart.inter():
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cd = form.cleaned_data
            send_spam_email.delay(cd['email'])
            # Очищаем корзину
            cart.clear()
            return render(request, 'order/order_created.html', {'order': order,})
    else:
        form = OrderCraeteForm()
        return render(request, 'order/order_create.html', {'cart': cart, 'form': form})
