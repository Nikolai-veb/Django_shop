from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review, Rating, ProductImages
from .forms import ReviewForm, RatingForm
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from cart.forms import CartAddProductForm


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
    star_form = RatingForm()
    cart_product_form = CartAddProductForm()
    form = ReviewForm()
    return render(request, "shop/product/product_detail.html", {'product': product,
                                                                'cart_product_form': cart_product_form,
                                                                'star_form': star_form,
                                                                'form': form,
                                                                })


def add_review(request, pk):
    """Отзовы"""
    product = Product.objects.get(id=pk, draft=False)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if  request.POST.get("parent", None):
                form.parent_id = (request.POST.get("parent"))
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())


def get_client_ip(self, request):
    """Получение клиенского ip"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_rating_star(self, request):
    """Добавление рейтинга к фильму"""
    if request.method == 'Post':
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                    ip=self.get_client_ip(request),
                    product_id=int(request.POST.get("product")),
                    defaults={'start_id':int(request.POST.get("start"))}
                    )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

