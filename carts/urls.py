from django.urls import path 
from . import views

urlpatterns = [
	path('cart', views.show_cart, name="cart"),
	path('update_cart', views.update_cart, name="cart.update"),
	path('remove_cart_product', views.remove_cart_product, name="cart.remove"),

]