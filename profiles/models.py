from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

# class User(AbstractUser):
# 	pass


class Profile(models.Model):
	user        = models.OneToOneField(User, on_delete=models.CASCADE)
	phone       = models.IntegerField(max_length=15, null=True)
	birth_date  = models.DateField(null=True, blank=True)
	city        = models.CharField(max_length=50,null=True)
	state       = models.CharField(max_length=50,null=True)
	country     = models.CharField(max_length=50,null=True)
	postal_code = models.IntegerField(null=True)
	created_at  = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at  = models.DateTimeField(auto_now_add=False, auto_now=True)
	status      = models.IntegerField(default=1)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
 	if created:
 		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()