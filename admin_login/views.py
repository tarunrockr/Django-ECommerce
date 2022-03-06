from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.template.response import TemplateResponse
from django.contrib import messages
# Create your views here.

# function to show login page
def admin_login(request):

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

		if user is not None:
			login(request,user)
			# Storing userdata in session
			request.session['user_id']    = user.id 
			request.session['email']      = user.email
			request.session['first_name'] = user.first_name
			request.session['last_name']  = user.last_name
			request.session['logged_in']  = True 

			# Redirecting to user profile page
			return HttpResponseRedirect(reverse('admin.dashboard'))
		else:
			messages.error("Username or password is invalid.")
			return HttpResponseRedirect(reverse('admin.login'))

	else:
		return redirect(reverse('admin.login'))