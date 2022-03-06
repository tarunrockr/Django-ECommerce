from django.urls import path 
from . import views

urlpatterns = [
	path('cart', views.show_cart, name="cart"),
	path('update_cart', views.update_cart, name="cart.update"),
	path('remove_cart_product', views.remove_cart_product, name="cart.remove"),
	path('add_cart_quantity', views.add_cart_quantity, name="cart.quantity.add"),
	path('remove_cart_quantity', views.remove_cart_quantity, name="cart.quantity.remove"),
	path('checkout_login_check', views.checkout_login_check, name="checkout.login_check"),
	path('checkout', views.checkout, name="checkout"),
	path('create_checkout_session', views.create_checkout_session, name="checkout.session"),
	path('stripe_webhook', views.stripe_webhook, name="stripe.webhook"),
	path('checkout_post', views.checkout_post, name="checkout.post"),
	path('checkout_success', views.checkout_success, name="checkout.success"),
	path('checkout_cancel', views.checkout_cancel, name="checkout.cancel"),
	path('add_shipping_address_ajax', views.add_shipping_address_ajax, name="add_shipping_address"),
	path('fetch_shipping_address_ajax', views.fetch_shipping_address_ajax, name="fetch_shipping_address"),

	# Ajax functions
	path('update_cart_logo_count', views.update_cart_logo_count, name='update_cart_logo_count'),
]