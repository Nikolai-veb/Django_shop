from django.contrib.auth import authenticate, login
from .forms import CustomUserRegisterForm, CustomUserEditForm, LoginForm
from .models import CustomUser
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, CreateView, UpdateView


class CustomerUserDetailView(DetailView):
    """Detail Customer User"""
    model = CustomUser
    context_object_name = "custom_user"
    pk_url_kwarg = 'pk'
    template_name = 'account/profile.html'


class RegisterCustomUserView(CreateView):
    """Register Users"""
    model = CustomUser
    form_class = CustomUserRegisterForm
    template_name = "account/register.html"
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        valid = super(RegisterCustomUserView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class EditCustomerUserView(UpdateView):
    """Edit Customer User"""
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'account/edit.html'
    pk_url_kwarg = "pk"


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/c_login.html"

# def register(request):
#     """Обработчик регистрации пользователя"""
#     if request.method == 'POST':
#         new_user_form = UserRegisterForm(request.POST)
#         if new_user_form.is_valid():
#             new_user_from = new_user_form.save(commit=false)
#             new_user_from.set_password(new_user_form.cleaned_data['password'])
#             # Создание Profile
#             new_user_from.save()
#             CustomUser.objects.create(username=new_user_form)
#             return render(request, 'account/register_done.html', {'new_user_from': new_user_from})
#     else:
#         new_user_form = UserRegisterForm()
#     return render(request, 'account/register.html', {'new_user_form': new_user_form})


# @login_required
# def edit(request):
#     """Оброботчик редактирования ппофиля"""
#     if request.method == 'POST':
#         # user_form = UserEditForm(instance=request.user, data=request.POST)
#         custom_user_form = CustomUserEditForm(instance=request.custom_user, data=request.POST, files=request.FILES)
#         if custom_user_form.is_valid():
#             custom_user_form.save()
#             return render(request, 'account/profile.html', {'custom_user_form': custom_user_form})
#     else:
#         custom_user_form = CustomUserEditForm(instance=request.custom_user)
#         return render(request, 'account/edit.html', {'custom_user_form': custom_user_form})


# @login_required
# def custom_users(request, id):
#     """Обработчик профиля"""
#     custom_user = get_object_or_404(CustomUser, id=id)
#     return render(request, 'account/profile.html', {'custom_user': custom_user})