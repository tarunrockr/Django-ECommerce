from django.urls import path 
from . import views

urlpatterns = [
	path('register', views.register_show, name='register.show'),
	path('register_post', views.register_post, name='register.post'),
	path('login', views.login_show, name='login.show'),
	path('login_post', views.login_post, name='login.post'),
] 