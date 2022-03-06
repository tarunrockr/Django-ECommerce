from django.urls import path 
from . import views


urlpatterns = [
	path('dashboard',views.dashboard, name="admin.dashboard"),
	path('testpage',views.test_function, name="admin.test")
]