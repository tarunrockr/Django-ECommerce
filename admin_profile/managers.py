from django.db import models

class CustomManager(models.Manager):

	# Here we are overriding the get_queryset method of built-in manager  
	# def get_queryset(self):
	# 	return super().get_queryset().order_by('name')

	# Here we are creating the custom method of our custom manager(CustomManager). 
	def get_stu_roll_range(self,r1,r2):
		return super().get_queryset().filter(roll__range = (r1,r2))