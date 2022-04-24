from django.urls import path 
from . import views

urlpatterns = [
	path('email_verification/<slug:hash>/<int:user_id>/', views.verify_email, name="email.verify"),
	path('verify_email/<int:user_id>/', views.verify_email_page, name="email.verify.page"),
	path('verify_email_resend', views.verify_email_resend, name="email.verify.resend")
]