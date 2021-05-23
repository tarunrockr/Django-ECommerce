from django.urls import path 
from . import views

urlpatterns = [
	path('cart', views.show_cart, name="cart"),
	path('update_cart', views.update_cart, name="cart.update"),
	path('remove_cart_product', views.remove_cart_product, name="cart.remove"),
	path('add_cart_quantity', views.add_cart_quantity, name="cart.quantity.add"),
	path('remove_cart_quantity', views.remove_cart_quantity, name="cart.quantity.remove"),
	path('checkout', views.checkout, name="checkout")
]