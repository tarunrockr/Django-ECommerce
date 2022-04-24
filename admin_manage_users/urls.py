from django.urls import path 
from . import views

urlpatterns = [
	path('adminlist', views.admin_userlist, name='admin.adminlist'),
	path('create_admin', views.create_admin_user, name='admin.create')
]