from django.urls import path 
from . import views


urlpatterns = [
	path('',views.login, name="admin.login"),
	path('login',views.login, name="admin.login"),
	path('login_post',views.login_post, name="admin.login.post")
]