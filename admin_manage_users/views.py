from django.shortcuts import render
from django.http      import HttpResponse, HttpResponseRedirect
from django.urls      import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db import connection
from admin_profile import common
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from random import randint
from django.core.mail import send_mail, EmailMessage
from django.utils.crypto import get_random_string
import hashlib
from django.template.loader import render_to_string

# Common class object
common_obj = common.Common(connection) 


@login_required( login_url = common_obj.this_group_login_url )
@user_passes_test( common_obj.check_user_group, login_url = common_obj.this_group_login_url )
def admin_userlist(request):

	groups = Group.objects.filter(id=4).values()
	return render(request, 'admin/manage_users/adminlist.html', {'groups': groups})

@login_required( login_url = common_obj.this_group_login_url )
@user_passes_test( common_obj.check_user_group, login_url = common_obj.this_group_login_url )
def create_admin_user(request):

	if request.method == "POST":

		first_name   = request.POST['first_name']
		last_name    = request.POST['last_name']
		username     = request.POST['username']
		email        = request.POST['email']
		group_id     = request.POST['group']
		phone        = request.POST['phone']
		raw_password = randint(10000000, 99999999)
		password     = make_password(raw_password)

		try:
			checkUser = User.objects.get(email=email)
		except:
			checkUser = None

		if checkUser is None:
			# creating the user
			user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
			user.profile.phone = phone
			user.save()

			# Getting the admin group object
			admin_group = Group.objects.get(name='admin')
			admin_group.user_set.add(user)

			# ------ Sending credentials to the user without html template  ----

			# setting the hash string before sending email to user (Attach to email url and store in the profile table that need to be match ata time of password reset)
			# Generate 32 digit random string
			random_str = get_random_string(length=32)
			hash_str   = hashlib.md5(random_str.encode()).hexdigest()

			# Updating the user account with the hash
			user_account = User.objects.get(id=user.pk)
			user_account.profile.hashstr = hash_str
			user_account.save()

			# # Create custom url that need to be send to user to reset password
			# # request.build_absolute_uri('/') gives 'http://localhost:8000/' for local
			# custom_url = request.build_absolute_uri('/')+'email_verification/'+str(hash_str)+"/"+str(user.id)+"/"
			# subject    = "E-Commerce account credentials and email verification"
			# message    = "Welcome "+first_name+" "+last_name+"\nYour temporary password is: "+str(raw_password)+"\n Click to verify the email: "+str(custom_url)
			# from_email = "info@ecom.com"
			# to_email   = [email]
			# #send_mail('<Your subject>', '<Your message>', 'from@example.com', ['to@example.com'])
			# send_mail(subject, message, from_email, to_email)  

			# ------ Sending credentials to the user with html template  ----
			subject    = "E-Commerce account credentials and email verification"
			from_email = "info@ecom.com"
			to_email   = [email]
			custom_url = request.build_absolute_uri('/')+'email_verification/'+str(hash_str)+"/"+str(user.id)+"/"
			html_message =  render_to_string('common/emails/emailtemplates/admin_verify_email.html', {'user': user, 'raw_password': raw_password, 'custom_url': custom_url})
			msg          =  EmailMessage(subject, html_message, from_email, to_email)
			msg.content_subtype = "html"
			msg.send()


			if user:
				messages.success(request, "User created successfully. Mail send to the user with account details.")
				return HttpResponseRedirect(reverse('admin.create'))
			else:
				messages.error(request, "Problem in creating admin user.")
				return HttpResponseRedirect(reverse('admin.create'))

		else:
			messages.error(request, "User already Registered")
			return HttpResponseRedirect(reverse('admin.create'))

	else:
		return HttpResponseRedirect(reverse('admin.adminlist'))

