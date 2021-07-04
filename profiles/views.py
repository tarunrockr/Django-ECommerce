from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile
from django.contrib.auth.models import User, auth
from django.urls import reverse
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required, user_passes_test
from profiles import signals

# Create your views here.

# def user_not_loggedin(user):
# 	# Return true is user is logged out
# 	return not user.is_authenticated

#@user_passes_test(user_not_loggedin, login_url='/user_profile')
def register_show(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('profile.dashboard'))

	return render(request, 'front/profiles/register.html', {})

#@user_passes_test(user_not_loggedin, login_url='/user_profile')
def register_post(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('profile.dashboard'))
	
	if request.method == "POST":

		first_name 		 = request.POST.get('first_name')
		last_name  		 = request.POST.get('last_name')
		mobile     		 = request.POST.get('mobile')
		email      		 = request.POST.get('email')
		password   		 = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')

		prev = {'first_name':first_name, 'last_name': last_name, 'mobile': mobile, 'email': email}

		error = {}
		if first_name == "":
			error['first_name'] = 'First Name Required' 
		if last_name == "":
			error['last_name'] = 'Last Name Required' 
		if mobile == "":
			error['mobile'] = 'Mobile Required' 
		if email == "":
			error['email'] = 'Email Required' 
		if password == "":
			error['password'] = 'Password Required' 
		if confirm_password == "":
			error['confirm_password'] = 'Confirm Password Required'
		if confirm_password != password:
			error['password_unmatch'] = 'Password Mismatch'

		if len(error) != 0:
			return render(request, 'front/profiles/register.html', {'error': error, 'prev': prev})

		try:
			checkUser = User.objects.get(email=email)
		except:
			checkUser = None

		if checkUser is None:
			user = User.objects.create_user(username = first_name, first_name = first_name, last_name = last_name, email= email, password = password)
			user.profile.phone = mobile
			user.save()

			if user:
				messages.success(request, "Success: Registered successfully. You can Login Now.")
				return HttpResponseRedirect(reverse('register.show'))
			else:
				messages.error(request, "Problem in register occured.")
				return HttpResponseRedirect(reverse('register.show'))
		else:
			messages.error(request, "User already Registerd.")
			return HttpResponseRedirect(reverse('register.show'))

#@user_passes_test(user_not_loggedin, login_url='/user_profile')
def login_show(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('profile.dashboard'))

	form = LoginForm()
	return render(request, 'front/profiles/login.html', {'form': form})

#@user_passes_test(user_not_loggedin, login_url='/user_profile')
def login_post(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('profile.dashboard'))
	
	if request.method == "POST":

		form = LoginForm(request.POST)
		if form.is_valid():

			email    = form.cleaned_data['email']
			password = form.cleaned_data['password']

			user = authenticate(request, email=email, password=password, login_type='frontend')

			if user is not None:
				login(request, user)
				# Storing userdata in session
				request.session['user_id']    = user.id 
				request.session['email']      = user.email
				request.session['first_name'] = user.first_name
				request.session['last_name']  = user.last_name
				request.session['logged_in']  = True 

				# Redirecting to user profile page
				return HttpResponseRedirect(reverse('profile.dashboard'))
			else:
				messages.error(request, "Email or Password is incorrect.")
				return render(request, 'front/profiles/login.html', {'form': form})

		else:
			messages.error(request, "Email or Password is invalid.")
			return render(request, 'front/profiles/login.html', {'form': form})

	else:

		form = LoginForm()
		return render(request, 'front/profiles/login.html', {'form': form})

def logout(request):

	auth.logout(request)
	messages.success(request,"Success: Logout successfully.")
	return HttpResponseRedirect(reverse('login.show'))

#@login_required(login_url = 'login.show')
@login_required()
def  user_profile(request):
	#return HttpResponse(request.session['email'])
	
	# Calling or sending notification signal
	signals.notification.send(sender = None, request=request, user=["Tarun","Kumar"])

	return render(request, 'front/profiles/profile_dashboard.html',{})
