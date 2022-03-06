from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.dispatch import Signal, receiver
from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete, pre_migrate, post_migrate
from django.core.signals import request_started, request_finished, got_request_exception

# Login signals , START

# We can use this signal to storing the user ip address or user count. Storing the session or cache after login
@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):
	print("----------- Logged in signal --------")
	print("Sender: ",sender)
	print("Request: ",request)
	print("User: ",user)
	print("User Password: ",user.password)
	print(f"Kwargs: {kwargs}")
# user_logged_in.connect(login_success, sender=User)


@receiver(user_logged_out, sender=User)
def logout_success(sender, request, user, **kwargs):
	print("----------- Logout signal --------")
	print("Sender: ",sender)
	print("Request: ",request)
	print("User: ",user)
	print("User Password: ",user.password)
	print(f"Kwargs: {kwargs}")
# user_logged_out.connect(logout_success, sender=User)


# We can use this signal to store the login attempts in log file. Also can use to allow user limited login attempts.
@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):
	print("----------- Login Failed signal --------")
	print("Sender: ",sender)
	print("Request: ",request)
	print("Credentials: ",credentials)
	print(f"Kwargs: {kwargs}")
# user_login_failed.connect(login_failed)

# Login signals , END

# Model signals , START

@receiver(pre_save, sender=User)
def before_saving_data(sender, instance, **kwargs):
	print("----------- Pre Save signal --------")
	print("Sender: ",sender)
	print("Instance: ",instance)
	print(f"Kwargs: {kwargs}")
# pre_save.connect(before_saving_data, sender=User)

@receiver(post_save, sender=User)
def after_saving_data(sender, instance, created, **kwargs):
	if created == True:
		print("----------- Post Save signal --------")
		print("New Record Created")
		print("Sender: ",sender)
		print("Instance: ",instance)
		print("Created: ",created)
		print(f"Kwargs: {kwargs}")
	else:
		print("Update Created")
		print("Sender: ",sender)
		print("Instance: ",instance)
		print("Created: ",created)
		print(f"Kwargs: {kwargs}")
# post_save.connect(after_saving_data, sender=User)

@receiver(pre_delete, sender=User)
def before_delete(sender, instance, **kwargs):
	print("----------- Pre Delete signal --------")
	print("Sender: ",sender)
	print("Instance: ",instance)
	print(f"Kwargs: {kwargs}")
# pre_delete.connect(before_delete, sender=User)

@receiver(post_delete, sender=User)
def after_delete(sender, instance, **kwargs):
	print("----------- Post Delete signal --------")
	print("Sender: ",sender)
	print("Instance: ",instance)
	print(f"Kwargs: {kwargs}")
# post_delete.connect(after_delete, sender=User)


# @receiver(pre_init, sender=User)
# def before_model_initialization(sender, *args, **kwargs):
# 	print("----------- Pre Init signal --------")
# 	print("Sender: ",sender)
# 	print(f"Args: {args}")
# 	print(f"Kwargs: {kwargs}")
# # pre_init.connect(before_model_initialization, sender=User)

# @receiver(post_init, sender=User)
# def after_model_initialization(sender, *args, **kwargs):
# 	print("----------- Post Init signal --------")
# 	print("Sender: ",sender)
# 	print(f"Args: {args}")
# 	print(f"Kwargs: {kwargs}")
# # post_init.connect(after_model_initialization, sender=User)


# Model signals , END


# Request-Response signals , START

# @receiver(request_started)
# def before_request_start(sender, environ, **kwargs):
# 	print("----------- Request Started signal --------")
# 	print("Sender: ",sender)
# 	print("Environ: ",environ)
# 	print(f"Kwargs: {kwargs}")
# # request_started.connect(before_request_start, sender=User)


# @receiver(request_finished)
# def after_request_finish(sender, **kwargs):
# 	print("----------- Request Finished signal --------")
# 	print("Sender: ",sender)
# 	print(f"Kwargs: {kwargs}")
# # request_finished.connect(after_request_finish, sender=User)

# @receiver(got_request_exception)
# def request_exception_case(sender, request, **kwargs):
# 	print("----------- Request Finished signal --------")
# 	print("Sender: ",sender)
# 	print("Request: ",request)
# 	print(f"Kwargs: {kwargs}")
# # got_request_exception.connect(request_exception_case, sender=User)

# Request-Response signals , END

# Request-Response signals , START

@receiver(pre_migrate)
def before_migration_start(sender, app_config, verbosity, interactive, using, plan, apps, **kwargs):
	print("----------- Pre Migration signal --------")
	print("Sender: ",sender)
	print("App config: ",app_config)
	print("Verbosity: ",verbosity)
	print("Interactive: ",interactive)
	print("Using: ",using)
	print("Plan: ",plan)
	print("Apps: ",apps)
	print(f"Kwargs: {kwargs}")

@receiver(post_migrate)
def after_migration(sender, app_config, verbosity, interactive, using, plan, apps, **kwargs):
	print("----------- Post Migration signal --------")
	print("Sender: ",sender)
	print("App config: ",app_config)
	print("Verbosity: ",verbosity)
	print("Interactive: ",interactive)
	print("Using: ",using)
	print("Plan: ",plan)
	print("Apps: ",apps)
	print(f"Kwargs: {kwargs}")

# Request-Response signals , END


# Custom signal , START

# Creating signal
notification = Signal(providing_args=["request","user"])

# Receiver function
@receiver(notification)
def show_notification(sender, **kwargs):
	print("------------------------------------------------")
	print("Notificaton signal is being send in profile page")
	print("Sender: ",sender)
	print(f"kwargs: {kwargs}")
	print("------------------------------------------------")
	

# Custom signal , END
	
	


# ------------------------------------------------------------------------------------------------------------







# from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
# from django.contrib.auth.models import User
# from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete
# from django.dispatch import receiver


# @receiver(user_logged_in, sender=User)
# def login_success(sender, request, user, **kwargs):

# 	print("Logged-In Signal ...")
# 	print("Sender: ",sender)
# 	print("Request: ",request)
# 	print("user: ",user)
# 	print("User Email: ",user.email)
# 	print(f'Kwargs {kwargs}')
# #user_logged_in.connect(login_success, sender=User)


# @receiver(user_logged_out, sender=User)
# def logout_success(sender, request, user, **kwargs):

# 	print("Logged-Out Signal ...")
# 	print("Sender: ",sender)
# 	print("Request: ",request)
# 	print("user: ",user)
# 	print("User Email: ",user.email)
# 	print(f'Kwargs {kwargs}')
# #user_logged_out.connect(logout_success, sender=User)


# @receiver(pre_save, sender=User)
# def pre_save_test(sender, instance, **kwargs):

# 	print("Pre save Signal Test ...")
# 	print("Instance: ",instance)
# 	print(f'Kwargs {kwargs}')
# #pre_save.connect(pre_save_test, sender=User)

# @receiver(post_save, sender=User)
# def post_save_test(sender, instance, created, **kwargs):

# 	if created:
# 		print("Post save Signal Test ...")
# 		print("New Record")
# 		print("Instance: ",instance)
# 		print("Created: ",created)
# 		print(f'Kwargs {kwargs}')
# 	else:
# 		print("Post save Signal Test ...")
# 		print("Update")
# 		print("Instance: ",instance)
# 		print("Created: ",created)
# 		print(f'Kwargs {kwargs}')
# #post_save.connect(post_save_test, sender=User)

# @receiver(pre_delete, sender=User)
# def before_delete(sender, instance, **kwargs):
# 	print("Pre delete Signal Test ...")
# 	print("Sender: ",sender)
# 	print("Instance: ",instance)
# 	print(f'Kwargs {kwargs}')

# #pre_delete.connect(before_delete, sender=User)


# @receiver(post_delete, sender=User)
# def after_delete(sender, instance, **kwargs):
# 	print("Post delete Signal Test ...")
# 	print("Sender: ",sender)
# 	print("Instance: ",instance)
# 	print(f'Kwargs {kwargs}')

# #post_delete.connect(after_delete, sender=User)