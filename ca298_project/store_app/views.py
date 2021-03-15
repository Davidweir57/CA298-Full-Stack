from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404, redirect
from .forms import *
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .permissions import admin_required

# Create your views here.


class Login(LoginView):
	authentication_form = UserLoginForm
	template_name = "login.html"


def logout_view(request):
	logout(request)
	return redirect('/')


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


def all_products(request):
	all_p = Product.objects.all()
	return render(request, 'all_products.html', {'products' : all_p})


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
			return render(request, 'single_product.html', {'product': new_product})
	else:
		form = ProductForm()
		return render(request, 'form.html', {'form': form})



#todo - fix this view
#@login_required()
#@admin_required()
#def Stockform(request):
#	if request.method == 'POST':
#		form = ProductStockForm(request.POST)
#		data = request.POST.dict()
#		if form.is_valid():
#			obj = ProductStock.objects.filter(product_id=data.get("product")).first()
#			if obj is None:
#				stock_update = form.save()
#				return render(request, 'stock.html', {'form': form, 'added': True})
#			else:
#				obj.stock = obj.stock + form.data['stock']
#				obj.save()
#				return render(request, 'stock.html', {'form': form, 'added': True})
#
#	else:
#		form = ProductStockForm()
#		return render(request, 'stock.html', {'form': form})


@login_required()
def add_to_basket(request, productid):
	user = request.user
	product = Product.objects.get(pk=productid)
	shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()

	if not shopping_basket:
		shopping_basket = ShoppingBasket(user_id=user).save()

	sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id, product_id=product.id).first()
	if sbi is None:
		sbi = ShoppingBasketItems(basket_id=shopping_basket, product_id=product.id).save()
	else:
		sbi.quantity = sbi.quantity + 1
		sbi.save()
	return render(request, 'single_product.html', {'product': product, 'added': True})


@login_required
def shopping_basket(request, userid):
	user = request.user
	shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()

	sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)

	if len(sbi) > 0:
		products = []
		for i in sbi:
			products.append((Product.objects.get(pk=i.product_id), i.quantity))
		return render(request, "shopping_basket.html", {'products': products})
	else:
		return render(request, "/")


@login_required
def checkout(request):
	user = request.user
	shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()

	if not shopping_basket:
		return redirect(request, "/")
	sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)

	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			order = form.save(commit=False)
			order.user_id = request.user
			order.save()
			order_items = []
			for basketitem in sbi:
				order_item = OrderItems(order_id=order, product_id=basketitem.product.id, quantity=basketitem.quantity)
				order_items.append(order_item)

			shopping_basket.delete()
			ShoppingBasket(user_id=user).save()
			return render(request, 'order_complete.html', {'order': order, 'items': order_items})
	else:
		form = OrderForm()
		return render(request, 'checkout.html', {'form': form, 'basket': shopping_basket, 'items': sbi})


def european_sword(request):
	products = Product.objects.filter(category_id=1)
	return render(request, 'european_swords.html', {'products': products})


def oriental_sword(request):
	products = Product.objects.filter(category_id=2)
	return render(request, 'oriental_swords.html', {'products': products})



