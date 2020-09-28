
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review, Rating, ProductImages
from .forms import ReviewForm, RatingForm
from cart.forms import CartAddProductForm
from account.models import Profile
from django.db.models import Max, Min
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_categories():
    categories = Category.objects.all()
    return categories



def product_list(request, category_slug=None):
    get_category = get_categories()
    max_price = Product.objects.all().aggregate(Max('price'))
    min_price = Product.objects.all().aggregate(Min('price'))
    products = Product.objects.filter(draft=False)
    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом возвращаем 1 страницу
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    category = None
    categories = Category.objects.all()
    profile = Profile.objects.all()
    cart_product_form = CartAddProductForm()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    return render(request, "shop/product/product_list.html", {'products': products,
                                                              'categories': categories,
                                                              'category': category,
                                                              'cart_product_form': cart_product_form,
                                                              'profile': profile,
                                                              'max_price': max_price,
                                                              'min_price': min_price,
                                                              'page': page,
                                                              'get_category': get_category,
                                                              })


def filter_products(request):
    """Фильтр продуктов"""
    filters = Product.objects.filter(price__in=request.GET.get_list("price"))
    return


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
            if request.POST.get("parent", None):
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
                defaults={'start_id': int(request.POST.get("start"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

# class BookmarkView(View):
#     # в данную переменную будет устанавливаться модель закладок, которую необходимо обработать
#     model = None
#
#     def post(self, request, pk):
#         # нам потребуется пользователь
#         user = auth.get_user(request)
#         # пытаемся получить закладку из таблицы, или создать новую
#         bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)
#         # если не была создана новая закладка,
#         # то считаем, что запрос был на удаление закладки
#         if not created:
#             bookmark.delete()
#
#         return HttpResponse(
#             json.dumps({
#                 "result": created,
#                 "count": self.model.objects.filter(obj_id=pk).count()
#             }),
#             content_type="application/json"
#         )
