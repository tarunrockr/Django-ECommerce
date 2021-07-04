from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login 
from django.urls import reverse
from django.template.response import TemplateResponse
# Create your views here.

# function to show login page
def login(request):

	# Generating exception manually for testing purpose
	# print("Exception Occured")
	# a=10/0
	print("In the view")
	context = {'heading_name': 'Login'}
	#return render(request, 'admin/login/login.html',context)
	# Process template response middleware only works when sending  TemplateResponse
	return TemplateResponse(request, 'admin/login/login.html',context)

def login_post(request):

	if request.method == "POST":
		email 	 = request.POST.get('email')
		password = request.POST.get('password')
		# Login process Start
		user = authenticate(request, email=email, password=password, login_type='backend')

	else:
		return redirect(reverse('admin.login'))