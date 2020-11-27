from django.shortcuts import render, get_object_or_404
from .forms import UserRegisterForm, ProfileEditForm, UserEditForm, LoginForm

from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


class CastomLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/c_login.html"


def register(request):
    """Обработчик регистрации пользователя"""
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user_from = user_form.save(commit=False)
            user_from.set_password(user_form.cleaned_data['password'])
            # Создание Profile
            Profile.objects.create(username=user_form)
            user_from.save()
            return render(request, 'account/register_done.html', {'user_from': user_from})
    else:
        user_form = UserRegisterForm()
        return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    """Оброботчик редактирования ппофиля"""
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'account/profile.html', {'profile_form': profile_form, 'user_form': user_form})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def profile(request, id):
    """Обработчик профиля"""
    profiles = get_object_or_404(Profile, id=id)
    return render(request, 'account/profile.html', {'profiles': profiles})
