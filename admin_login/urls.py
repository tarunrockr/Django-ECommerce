from django.urls import path 
from . import views


urlpatterns = [
	path('',views.admin_login, name="admin.login"),
	path('login',views.admin_login, name="admin.login"),
	path('login_post',views.login_post, name="admin.login.post"),
	path('admin_logout', views.admin_logout, name='admin.logout')
]