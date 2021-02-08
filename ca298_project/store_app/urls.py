from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('registration/', views.register, name="register"),
	path('allproducts/', views.all_products, name='all_products'),
	path('product/<int:prodid>', views.singleproduct, name='single_product'),
	path('myform', views.myform)

]