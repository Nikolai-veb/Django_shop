from django.shortcuts import render, get_object_or_404

from .models import Category, Product, Review, Rating, ProductImages


def product_list(request, category_slug=None):
    products = Product.objects.filter(draft=False)
    category = None
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    return render(request, "shop/product/product_list.html", {'products':products,
                                                         'categories':categories,
                                                         'category':category,
                                                         })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, draft=False)
    return render(request, "shop/product/product_detail.html", {'product':product})


