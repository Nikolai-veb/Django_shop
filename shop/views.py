from django.shortcuts import render, get_object_or_404, redirect

from .models import Category, Product, Review, Rating, ProductImages
from .forms import ReviewForm
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

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
    return render(request, "shop/product/product_detail.html", {'product':product,})


class AddReview(View):
    """ Отзовы """
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk, draft=False)
        if form.is_valid():
            form = form.save(commit=False)
            if  request.POST.get("parent", None):
                form.parent_id =init(request.POST.get("parent"))
                form.product = product
                form.save()
        return redirect(product.get_absolute_url())


class AddStarRating(View):
    """Добавление рейтинга к фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    def post(self, request):
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

