from django.urls import path
from . import views, forms

urlpatterns = [
	path('', views.index, name="index"),
	path('allproducts/', views.all_products, name='all_products'),
	path('product/<int:prodid>', views.singleproduct, name='single_product'),
	path('myform', views.myform),
	path('usersignup/', views.CaUserSignupView.as_view(), name='register'),
	path('adminsignup/', views.CaAdminSignupView.as_view(), name='admin-register'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.logout_view, name="logout"),
	path('addbasket/<int:productid>', views.add_to_basket, name='add-basket'),
	path('basket/<int:userid>', views.shopping_basket, name='shopping_basket'),
	path('category/<int:cat_id>/', views.categories, name='product category page'),
	path('subcategory/<int:sub_id>/', views.subcategories, name='product subcategory page'),
	path('checkout', views.checkout, name="checkout"),
	#path('stock', views.Stockform)

]
