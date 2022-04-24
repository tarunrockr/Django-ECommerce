from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.template.response import TemplateResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import auth, User, Group, Permission
from admin_profile.models       import Groupinfo
from django.db     import connection
from admin_profile import common
# Create your views here.


# Common class object
common_obj = common.Common(connection)

# function to show login page
def admin_login(request):

	if request.user.is_authenticated:
		dashboard_url = common_obj.redirect_to_dashboard(request)
		return HttpResponseRedirect(dashboard_url)
		
	else:
		context = {'heading_name': 'Login'}
		# return render(request, 'admin/login/login.html',context)
		# Process template response middleware only works when sending  TemplateResponse
		return TemplateResponse(request, 'admin/login/login.html',context)


def login_post(request):

	if request.user.is_authenticated:
		dashboard_url = common_obj.redirect_to_dashboard(request)
		return HttpResponseRedirect(dashboard_url)
		
	else:
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
				messages.error(request, "Username or password is invalid.")
				return HttpResponseRedirect(reverse('admin.login'))

		else:
			return redirect(reverse('admin.login'))


@login_required( login_url = common_obj.this_group_login_url )
@user_passes_test( common_obj.check_user_group, login_url = common_obj.this_group_login_url )
def admin_logout(request):
	auth.logout(request)
	messages.success(request, "Logged out successfully.")
	return HttpResponseRedirect(reverse('admin.login'))
