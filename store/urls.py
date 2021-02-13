from django .urls import path 
from .import views

urlpatterns = [
	path('', views.home, name='home'),
	path('products', views.products, name='products'),
	path('products_ajax', views.fetch_products_ajax, name='products.fetch.ajax')
]