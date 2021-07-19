from django.db import models
from .managers import CustomManager

# Create your models here.




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



# Example of custom manager
class TestStudent(models.Model):
	name = models.CharField(max_length=200)
	roll = models.IntegerField()

	# Default manager of django
	objects = models.Manager()

	# Changed manager name to 'students' of django (Custom: created by us)
	# students= models.Manager()

	# Using custom manager from managers file
	students  = CustomManager()




