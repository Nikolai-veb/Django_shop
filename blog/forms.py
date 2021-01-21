from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """Comment form"""
    class Meta:
        model = Comment
        fields = ("name", "email", "text",)
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control border"}),
            "email": forms.EmailInput(attrs={"class":"form-control border"}),
            "text": forms.Textarea(attrs={"class":"form-control border"}),

        }

class ShareArticleForm(forms.Form):
    """Share email form"""
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control border"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control border"}))
    comments = forms.CharField(required=False ,widget=forms.Textarea(attrs={"class": "form-control border"}))

