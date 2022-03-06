from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Profile
from django.contrib.auth.models import User, auth
from django.urls import reverse
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required, user_passes_test
from profiles import signals
from carts.models import Cart, CartItem
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.db.models import Q
import ast
import decimal
import sys

# Create your views here.

# def user_not_loggedin(user):
# 	# Return true is user is logged out
# 	return not user.is_authenticated

#@user_passes_test(user_not_loggedin, login_url='/user_profile')
def register_show(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('profile.dashboard', kwargs={'tab_id': 1}))

	return render(request, 'front/profiles/register.html', {})

#@user_passes_test(user_not_loggedin, login_url='/user_profile')
def register_post(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('profile.dashboard', kwargs={'tab_id': 1}))
	
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

	# new_hash_password = make_password('123456')
	# return HttpResponse(new_hash_password)

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('profile.dashboard', kwargs={'tab_id': 1}))

	form = LoginForm()
	return render(request, 'front/profiles/login.html', {'form': form})

#@user_passes_test(user_not_loggedin, login_url='/user_profile')
def login_post(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('profile.dashboard', kwargs={'tab_id': 1}))
	
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

				# Storing the cart data from the cookies to database cart table

				if( 'cart' in request.COOKIES.keys() and len(request.COOKIES['cart']) > 0 ):

					cookie_data = request.COOKIES['cart']
					# using ast.literal_eval() convert dictionary string to dictionary
					cookie_data = ast.literal_eval(cookie_data)

					# Inserting the row in cart table
					cart, created = Cart.objects.get_or_create(user_id=user.id)

					cart_total = 0.00
					for key, value in cookie_data.items():
						product_id = int(key)
						# Get current product data in cart item table
						try:
							current_product_data = CartItem.objects.get(cart_id = cart.pk , product_id = product_id)
						except CartItem.DoesNotExist:
							current_product_data = None

						# Inserting the cart products
						if current_product_data == None:
							cart_item = CartItem.objects.create(quantity = value['product_quantity'], product_total = value['product_total'], product_id = product_id, cart_id = cart.pk )
							cart_total += float(value['product_total'])
						else:
							current_product_data.quantity += value['product_quantity']
							current_product_data.product_total += decimal.Decimal(value['product_total'])
							current_product_data.save()
							cart_total += float(current_product_data.product_total)	

					# Updating the total cart value 
					cart       = Cart.objects.get(pk=cart.pk)
					cart.total = cart_total
					cart.save()

				# Redirecting to user profile page
				response = HttpResponseRedirect(reverse('profile.dashboard', kwargs={'tab_id': 1}))
				response.delete_cookie('cart')
				return response
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
def  user_profile(request,tab_id):
	#return HttpResponse(request.session['email'])
	
	# Calling or sending notification signal
	signals.notification.send(sender = None, request=request, user=["Tarun","Kumar"])

	# Fetching user profile data 
	if tab_id ==1:
		user_data = User.objects.get(pk=request.user.id)
		context = {'tab_id': tab_id, 'user_data': user_data}
	else:
		context = {'tab_id': tab_id}

	return render(request, 'front/profiles/profile_dashboard.html', context)

@login_required
def user_profile_update(request):

	if request.method == "POST":

		first_name    = request.POST['first_name']
		last_name     = request.POST.get('last_name')
		username      = request.POST.get('username')
		date_of_birth = request.POST.get('date_of_birth') 
		gender        = request.POST.get('gender')  
		phone         = request.POST.get('phone')
		email         = request.POST.get('email')  
		date_of_birth = datetime.strptime( date_of_birth, '%Y/%m/%d').strftime("%Y-%m-%d")

		try:
			# Updating the user model
			User.objects.filter(id = request.user.id).update(first_name = first_name, last_name = last_name, username = username, email = email)
			# Updating the profile model
			Profile.objects.filter(user_id = request.user.id).update(phone = phone, gender = gender, birth_date = date_of_birth)
		except:
			messages.error(request, "Technical error occured when updating the User Model")
			return HttpResponseRedirect(reverse('profile.dashboard', kwargs = {'tab_id': 1}))

		messages.success(request, "Profile updated successfully")
		return HttpResponseRedirect(reverse('profile.dashboard', kwargs={'tab_id': 1}))

	else:
		return HttpResponseRedirect(reverse('profile.dashboard', kwargs = {'tab_id': 1}))

	return HttpResponse('profile update function')
	
@login_required()
def change_password(request):

	return render(request, 'front/profiles/change_password.html', {})

@login_required
def change_password_post(request):

	if request.method == "POST":

		current_password = request.POST.get('current_password')
		new_password     = request.POST.get('new_password')	
		confirm_password = request.POST.get('confirm_password')

		# getting the current logged in user password
		current_user_password = request.user.password 

		# Checking password
		password_match = check_password(current_password, current_user_password)

		if password_match:
			# Hashing the new password
			new_hash_password = make_password(new_password)

			# Setting the new password
			User.objects.filter(pk=request.user.id).update(password=new_hash_password)

			messages.success(request, 'Password changed successfully.')
			return HttpResponseRedirect(reverse('profile.change_password'))

		else:
			messages.error(request, 'Current password is wrong.')
			return HttpResponseRedirect(reverse('profile.change_password'))

	else:
		pass


# Function to check the existance of username
@login_required
def check_username(request):

	username = request.POST['username']
	user_id  = request.user.id
	users_count = User.objects.filter( Q(username = username) & ~Q(id=user_id) ).count()

	data = [{'users_count': users_count}]
	return JsonResponse(data, safe=False)