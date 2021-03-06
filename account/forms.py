from django import forms
from  .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-account", "id": "exampleInputEmail1"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control form-account", "id": "exampleInputPassword1"}))


class CustomUserRegisterForm(forms.ModelForm):
    """Форма регистрацыи"""
    password = forms.CharField(label="Пороль", widget=forms.PasswordInput(attrs={"class": "form-control border", "id": ""}))
    password2 = forms.CharField(label="Повторите Пороль", widget=forms.PasswordInput(attrs={"class": "form-control border", "id": ""}))

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', "avatar", "date_birth")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control border", "id": ""}),
            "first_name": forms.TextInput(attrs={"class": "form-control border", "id": ""}),
            "last_name": forms.TextInput(attrs={"class": "form-control border", "id": ""}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "avatar": forms.FileInput(),
            "date_birth": forms.DateInput(attrs={"class": "form-control border"})
        }

    def is_valid(self):
        image = super(CustomUserRegisterForm, self).is_valid()
        image_avatar = self.cleaned_data['avatar']
        expansion_avatar = (str(image_avatar).split('.')[-1])
        expansions = ['jpeg', 'jpg', 'png']
        if image_avatar and expansion_avatar not in expansions:
            raise forms.ValidationError('Your file is not an image or has the wrong extension !!! \n Available extensions jpeg, jpg, png')
        else:
            return self.is_bound

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        elif len(cd['password']) < 8:
            raise forms.ValidationError('Пароль слишком короткий')
        return cd['password2']

    def save(self, commit=True) :
        # Save the provided password in hashed format
        user = super(CustomUserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data[ "password" ])
        my_group = Group.objects.get(name='Visitors')
        if commit:
            user.save()
            # my_group.user_set.add(user)
        return user


class CustomUserEditForm(forms.ModelForm):
    """Форма для редоктирования созданных полей """

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', "avatar", "date_birth")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control border", "id": ""}),
            "first_name": forms.TextInput(attrs={"class": "form-control border", "id": ""}),
            "last_name": forms.TextInput(attrs={"class": "form-control border", "id": ""}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "avatar": forms.FileInput(),
            "date_birth": forms.DateInput(attrs={"class": "form-control border"})
        }

    def is_valid(self):
        image = super(CustomUserEditForm, self).is_valid()
        image_avatar = self.cleaned_data['avatar']
        expansion_avatar = (str(image_avatar).split('.')[-1])
        expansions = ['jpeg', 'jpg', 'png']
        if image_avatar and expansion_avatar not in expansions:
            raise forms.ValidationError('Your file is not an image or has the wrong extension !!! \n Available extensions jpeg, jpg, png')
        else:
            return self.is_bound