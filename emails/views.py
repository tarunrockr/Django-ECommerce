from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group 
from django.db import connection 
from django.urls import reverse
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
import json
import hashlib


# Create your views here.

# For superadmin and admin user

def verify_email(request,hash,user_id):

	# Fetch the user
	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		user = None

	if user:
		hashstr =  user.profile.hashstr

		if user.profile.email_verify == 0:

			if hashstr != None:

				if(hashstr == hash):

					# updating the email_verify field in user profile 
					user.profile.email_verify = 1
					user.profile.hashstr      = None
					user.save()

					# If hash string matches then fetch the group and redirect to login page of respective group
					cursor = connection.cursor()
					sql = "SELECT * FROM auth_user_groups WHERE user_id="+str(user_id)+" LIMIT 1 "
					cursor.execute(sql)
					user_group = cursor.fetchone()
					group_id   = user_group[2]

					# For superadmin and admin user
					if group_id in [1,4]:
						messages.success(request, "Your email verified successfully. You can login now.")
						return HttpResponseRedirect(reverse('admin.login'))

					# For customer user
					elif group_id in [2]:
						messages.success(request, "Your email verified successfully. You can login now.")
						return HttpResponseRedirect(reverse('login.show'))

					# For seller user
					elif group_id in [3]:
						pass

				else:
					pass
			else:
				return HttpResponse('Link has been expired')
		else:
			return HttpResponse('Email already verified')
		
	else:
		pass


# To handle various conditions while handling verify email.
def verify_email_page(request, user_id):


	template = "common/emails/verify_email.html"
	return render(request, template, {'user_id': user_id})


# Resent email to verify user email
def verify_email_resend(request):

	user_id = request.POST.get('user_id','')
	
	# Fetch user data 
	user = User.objects.get(pk=2);

	random_str = get_random_string(length = 32)
	hash_str      = hashlib.md5(random_str.encode()).hexdigest() 

	# Updating the user account with the hash
	user.profile.hashstr = hash_str
	user.save()

	# ------ Sending credentials to the user with html template  ----
	subject    = "E-Commerce account email verification"
	from_email = "info@ecom.com"
	to_email   = [user.email]
	#to_email   = ['test444@yopmail.com']
	custom_url = request.build_absolute_uri('/')+'email_verification/'+str(hash_str)+"/"+str(user_id)+"/"
	html_message =  render_to_string('common/emails/emailtemplates/admin_verify_email.html', {'user': user, 'raw_password': None, 'custom_url': custom_url})
	msg          =  EmailMessage(subject, html_message, from_email, to_email)
	msg.content_subtype = "html"
	msg.send()

	data = {'user_id': user.email}
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type="application/json")
	






