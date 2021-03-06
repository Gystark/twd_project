from django import forms
from django.contrib.auth.models import User

from .models import Category, Page, UserProfile


class CategoryForm(forms.ModelForm):
    """
    A simple form for adding categories to Rango.
    """
    name = forms.CharField(max_length=128, help_text = "Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ("name", )


class PageForm(forms.ModelForm):
    """
    Simple form for adding pages to Rango
    """
    title = forms.CharField(max_length=128, help_text = "Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text = "Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        fields = ("title", "url")

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data


class UserForm(forms.ModelForm):
    """
    A simple user login form.
    """
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    """
    A simple user profile form
    """
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
