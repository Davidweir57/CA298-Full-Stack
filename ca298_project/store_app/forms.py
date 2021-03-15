from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction


class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ProductChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ProductForm(ModelForm):
    category = CategoryChoiceField(queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'picture', 'category']


class ProductStockForm(ModelForm):

    product = ProductChoiceField(queryset=Product.objects.all())

    class Meta:
        model = ProductStock
        fields = ['stock', 'product']


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

    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_addr', 'card_num']
