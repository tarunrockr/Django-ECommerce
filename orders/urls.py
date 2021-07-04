from django.urls import path 
from . import views

urlpatterns = [
	path('orders', views.order_list, name="orders"),
	path('orders_data_ajax', views.orders_data_ajax, name="orders_data_ajax"),

]