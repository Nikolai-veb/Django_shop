from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from shop.models import Product
from .bookmarks import Favorites
#from .forms import FavoriteAddProductForm

@require_GET
def favorite_add(request, product_id):
    favorite = Favorites(request)
    product = get_object_or_404(Product, id=product_id)
    favorite.add(product=product)
    return redirect('favorite_detail')


def favorite_remove(request, product_id):
    favorite = Favorites(request)
    product = get_object_or_404(Product, id=product_id)
    favorite.remove(product)
    return redirect('favorite_detail')


def favorite_detail(request):
    favorite = Favorites(request)
    return render(request, 'favorites/favorite_detail.html', {'favorite': favorite})
