from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.utils.decorators import method_decorator

from .models import *
from django.shortcuts import get_object_or_404, redirect
from .forms import *
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .permissions import admin_required
from rest_framework import viewsets
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
import json
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


class Login(LoginView):
    authentication_form = UserLoginForm
    template_name = "login.html"


def logout_view(request):
    logout(request)
    return redirect('/')


@method_decorator(csrf_exempt, name='dispatch')
class CaUserSignupView(CreateView):
    model = CaUser
    form_class = CaSignupForm
    template_name = 'causer_signup.html'


    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class CaAdminSignupView(CreateView):
    model = CaUser
    form_class = AdminSignupForm
    template_name = 'admin_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def index(request):
    return render(request, 'index.html')


def singleproduct(request, prodid):
    product = get_object_or_404(Product, pk=prodid)
    return render(request, 'single_product.html', {'product': product})


@login_required()
@admin_required()
def myform(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save()
            return render(request, 'form.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'form.html', {'form': form})


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_to_basket(request, productid):
    user = request.user
    if user.is_anonymous:
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        user = Token.objects.get(key=token).user
    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()
    if not shopping_basket:
        shopping_basket = ShoppingBasket(user_id=user).save()
    # TODO: handle product ID gracefully
    # get shopping basket
    product = Product.objects.get(pk=productid)
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id, product_id=product.id).first()
    if sbi is None:
        sbi = ShoppingBasketItems(basket_id=shopping_basket, product_id=product.id).save()
    else:
        sbi.quantity = sbi.quantity+1
        sbi.save()
    flag = request.GET.get('format', '')  # url?format=json&name=John   {'format':'json', 'name':'John'}
    if flag == "json":
        return JsonResponse({'status': 'success'})
    else:
        return render(request, 'single_product.html', {'product': product, 'added': True})


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def shopping_basket(request):
    user = request.user
    if user.is_anonymous:
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        user = Token.objects.get(key=token).user
    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()
    if not shopping_basket:
        shopping_basket = ShoppingBasket(user_id=user).save()
        return render(request, "shopping_basket.html", {'empty': True})
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)
    flag = request.GET.get('format', '')  # url?format=json&name=John   {'format':'json', 'name':'John'}
    if flag == "json":
        basket_array = []
        for basket_item in sbi:
            tmp = {}
            tmp['product'] = basket_item.product.name
            tmp['price'] = float(basket_item.product.price)
            tmp['quantity'] = int(basket_item.quantity) # [{'name':'price': 'quantity': },{}]
            basket_array.append(tmp)
        return HttpResponse(json.dumps({'items': basket_array}), content_type="application/json")
    else:
        return render(request, 'shopping_basket.html', {'basket': shopping_basket, 'products': sbi})


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def checkout(request):
    user = request.user
    if user.is_anonymous:
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        user = Token.objects.get(key=token).user
    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()
    if not shopping_basket:
        return redirect(request, 'shopping_basket.html', {'empty': True})
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)
    if request.method == 'POST':
        if not request.POST: # if the data is not inside the request.POSt, it is inside the body
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            form = OrderForm(body)
        else:
            form = OrderForm(request.POST)
        print(form.errors)
        if form.is_valid():
            # create order item for each order in shopping basket

            order = form.save(commit=False)
            order.user_id = user
            order.save()
            order_items = []
            for basketitem in sbi:
                order_item = OrderItems(order_id=order, product=basketitem.product, quantity=basketitem.quantity)
                order_items.append(order_item)
            # delete the shopping basket
            shopping_basket.delete()
            flag = request.GET.get('format', '')  # url?format=json&name=John   {'format':'json', 'name':'John'}
            if flag == "json":
                return JsonResponse({"status": "success"})
            else:
                return render(request, 'order_complete.html', {'order': order, 'items':order_items})
    else:
        form = OrderForm()
        return render(request, 'checkout.html', {'form': form, 'basket':shopping_basket, 'items': sbi})


def categories(request, cat_id):
    products = Product.objects.filter(category_id=cat_id)
    subcategory = ProductSubCategory.objects.filter(parent_id=cat_id)
    return render(request, 'productcategory.html', {'products': products, 'subcategories': subcategory})


def subcategories(request, sub_id):
    products = Product.objects.filter(subcategory_id=sub_id)
    subcategory = ProductSubCategory.objects.filter(parent_id=products[0].category_id)
    return render(request, 'productcategory.html', {'products': products, 'subcategories': subcategory})


class UserViewSet(viewsets.ModelViewSet):
    queryset = CaUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []


