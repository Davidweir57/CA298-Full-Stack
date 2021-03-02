from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction


class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ProductForm(ModelForm):
    category = CategoryChoiceField(queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'picture', 'category']


class CaSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CaUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user


class AdminSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CaUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.TextInput()
    password = forms.CharField(widget=forms.PasswordInput)
