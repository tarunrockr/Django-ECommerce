from django.db import models
from .managers import CustomManager
from django.contrib.auth.models import User, Group

# Create your models here.

class Groupinfo(models.Model):
	group         = models.OneToOneField(Group, on_delete=models.CASCADE)
	description   = models.TextField(null=True, blank=True)
	dashboard_url = models.CharField(null=True, blank=True, max_length=255) 
	login_url     = models.CharField(null=True, blank=True, max_length=255) 



# Just for testing purpose. Not related to project
# # ------------------- Example of Model inheritance ( Using Abstract Parent(Base) class) --------------

# # Abstract Class(This class will not create any database table )
# class CommonInfo(models.Model):
# 	name = models.CharField(max_length=200)
# 	age  = models.IntegerField()
# 	date = models.DateField()

# 	class Meta:
# 		abstract = True


# # child class inheriting CommonInfo class
# class Student(CommonInfo):
# 	fees = models.IntegerField()
# 	# After defining date = None , it will not inherit date from CommonInfo class
# 	date = None

# # child class inheriting CommonInfo class
# class Teacher(CommonInfo):
# 	salary = models.IntegerField()

# # child class inheriting CommonInfo class
# class Contractor(CommonInfo):
# 	# After defining date = models.DateTimeField() , it will override date from CommonInfo class
# 	date   = models.DateTimeField()
# 	payment= models.IntegerField()



# # ------------------------ Proxy model ------------------------
# # Main model for employee
# class Employee(models.Model):
# 	 	name = models.CharField(max_length=200)
# 	 	age  = models.IntegerField()

# # This is an proxy class( This class will not create a DB table)
# # We can use this proxy class to access employee table also. We can also apply change ordering, filtering differently than Employee Model 
# class MyEmployee(Employee):
# 	class Meta:
# 		proxy = True



# Test Example of custom manager
class TestStudent(models.Model):
	name = models.CharField(max_length=200)
	roll = models.IntegerField()

	# Default manager of django
	objects = models.Manager()

	# Changed manager name to 'students' of django (Custom: created by us)
	# students= models.Manager()

	# Using custom manager from managers file
	students = CustomManager()


# Test for query lookups in ORM like lt,gt,exact,contains

class Dummy(models.Model):
	name = models.CharField(max_length=200)
	roll = models.IntegerField(unique = True, null=False)
	city = models.CharField(max_length=200)
	marks= models.IntegerField()
	passdate = models.DateField()
	ndatetime = models.DateTimeField()



# Test model for One To One Relationship
# class Page(models.Model):

# 	user = models.OneToOneField(User,on_delete=models.CASCADE)
# 	page_name = models.CharField(max_length=200)
# 	page_category = models.CharField(max_length=200)
# 	publish_date = models.DateTimeField()


# Test model for Many To Many Relationship
class TestSong(models.Model):

	user      = models.ManyToManyField(User)
	song_name = models.CharField(max_length=200)
	song_date = models.DateTimeField()




