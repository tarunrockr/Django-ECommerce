from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile
from django.contrib.auth.models import User, auth
from django.urls import reverse
from django.contrib import messages

# Create your views here.

def register_show(request):
	
	return render(request, 'front/profiles/register.html', {})

def register_post(request):
	
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
		


def login_show(request):
	pass
	# render(request, '', {})

def login_post(request):
	pass
	# render(request, '', {})
