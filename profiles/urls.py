from django.urls import path 
from . import views

urlpatterns = [
	path('register', views.register_show, name='register.show'),
	path('register_post', views.register_post, name='register.post'),
	path('login', views.login_show, name='login.show'),
	path('login_post', views.login_post, name='login.post'),
	path('user_profile/<int:tab_id>/', views.user_profile, name='profile.dashboard'),
	path('user_profile_update/', views.user_profile_update, name='profile.update'),
	path('change_password', views.change_password, name='profile.change_password'),
	path('change_password_post', views.change_password_post, name='profile.change_password_post'),
	path('check_username', views.check_username, name='username.check'),
	path('logout', views.logout, name='logout'),

	
] 