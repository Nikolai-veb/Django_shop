from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-account", "id": "exampleInputEmail1"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control form-account", "id": "exampleInputPassword1"}))


class UserRegisterForm(forms.ModelForm):
    """Форма регистрацыи"""
    password = forms.CharField(label="Пороль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите Пороль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            "username": forms.TextInput(attrs={"class": "", "id": ""}),
            "first_name": forms.TextInput(attrs={"class": "", "id": ""}),
            "last_name": forms.TextInput(attrs={"class": "", "id": ""}),
            "email": forms.EmailInput(attrs={"class": ""}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """Форма для редактирования встроенных полей"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """Форма для редоктирования созданных полей """

    class Meta:
        model = Profile
        fields = ('photo', 'date_birth')
