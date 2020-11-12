from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review, Rating, ProductImages
from .forms import ReviewForm, RatingForm, SorteProductForm
from cart.forms import CartAddProductForm
from account.models import Profile
from django.db.models import Max, Min, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_GET, require_POST
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from django.contrib.postgres.search import TrigramSimilarity


class PriceCategory:

    def get_category(self):
        return Category.objects.all()

    def get_price(self):
        return Product.objects.filter(draft=False).values('price')

    def min_price(self):
        return Product.objects.all().aggregate(Min('price'))

    def max_price(self):
        return Product.objects.all().aggregate(Max('price'))


class ProductListView(PriceCategory, ListView):
    """Класс обработки продуктов"""
    model = Product
    template_name = "shop/product/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs
        queryset = Product.objects.filter(draft=False)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug['slug'])
            queryset = Product.objects.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cart_product_form'] = CartAddProductForm()
        context['profile'] = Profile.objects.all()
        return context


class ProductDetailView(PriceCategory, DetailView):
    """Класс обрботки продукта"""
    model = Product
    id_field = "pk"
    template_name = "shop/product/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context["cart_product_form"] = CartAddProductForm()
        context["form"] = ReviewForm()
        return context


class FilterProduct(PriceCategory, ListView):
    """Фильтр продустов"""
    template_name = "shop/product/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        price_range = [i for i in range(int(self.request.GET['min_price']), int(self.request.GET['max_price']))]
        queryset = Product.objects.filter(Q(category__in=self.request.GET.getlist("category")) |
                                          Q(price__in=price_range)
                                          )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        return context


class SorteProduct(PriceCategory, ListView):
    """Сортировка продукта"""
    template_name = "shop/product/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        sort = [i for i in self.request.GET.keys()][:-1]
        queryset = Product.objects.order_by(*sort)
        return queryset


class SearchProduct(ListView):
    """Поиск продукта"""
    template_name = "shop/product/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.annotate(
            similarity=TrigramSimilarity('name', self.request.GET.get('q')),
        ).filter(similarity__gt=0.3).order_by('-similarity')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class AddReview(View):
    """Отзовы"""

    def post(self, request, pk):
        product = Product.objects.get(id=pk, draft=False)
        form = ReviewForm(self.request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if self.request.POST.get("parent", None):
                form.parent_id = (self.request.POST.get("parent"))
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
                defaults={'start_id': int(request.POST.get("start"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
