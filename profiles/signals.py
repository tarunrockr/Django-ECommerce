from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.db.models.signals import pre_init, pre_save, pre_delete, post_init, post_save, post_delete
from django.dispatch import receiver


@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):

	print("Logged-In Signal ...")
	print("Sender: ",sender)
	print("Request: ",request)
	print("user: ",user)
	print("User Email: ",user.email)
	print(f'Kwargs {kwargs}')
#user_logged_in.connect(login_success, sender=User)


@receiver(user_logged_out, sender=User)
def logout_success(sender, request, user, **kwargs):

	print("Logged-Out Signal ...")
	print("Sender: ",sender)
	print("Request: ",request)
	print("user: ",user)
	print("User Email: ",user.email)
	print(f'Kwargs {kwargs}')
#user_logged_out.connect(logout_success, sender=User)


@receiver(pre_save, sender=User)
def pre_save_test(sender, instance, **kwargs):

	print("Pre save Signal Test ...")
	print("Instance: ",instance)
	print(f'Kwargs {kwargs}')
#pre_save.connect(pre_save_test, sender=User)

@receiver(post_save, sender=User)
def post_save_test(sender, instance, created, **kwargs):

	if created:
		print("Post save Signal Test ...")
		print("New Record")
		print("Instance: ",instance)
		print("Created: ",created)
		print(f'Kwargs {kwargs}')
	else:
		print("Post save Signal Test ...")
		print("Update")
		print("Instance: ",instance)
		print("Created: ",created)
		print(f'Kwargs {kwargs}')
#post_save.connect(post_save_test, sender=User)

@receiver(pre_delete, sender=User)
def before_delete(sender, instance, **kwargs):

	print("Pre delete Signal Test ...")
	print("Sender: ",sender)
	print("Instance: ",instance)
	print(f'Kwargs {kwargs}')

#pre_delete.connect(before_delete, sender=User)


@receiver(post_delete, sender=User)
def after_delete(sender, instance, **kwargs):

	print("Post delete Signal Test ...")
	print("Sender: ",sender)
	print("Instance: ",instance)
	print(f'Kwargs {kwargs}')

#post_delete.connect(after_delete, sender=User)