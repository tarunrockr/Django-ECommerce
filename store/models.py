from django.db import models

# Create your models here.

class Category(models.Model):

	name         = models.CharField(max_length=100, null=True)
	created_at   = models.DateTimeField(auto_now_add=True)
	updated_at   = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Product(models.Model):

	name         = models.CharField(max_length=100, null=True)
	price        = models.IntegerField(default=0)
	category     = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	description  = models.CharField(max_length=255, default='', null=True, blank=True)
	image        = models.ImageField(upload_to='upload/products/')
	status       = models.IntegerField(default=1)
	created_at   = models.DateTimeField(auto_now_add=True)
	updated_at   = models.DateTimeField(auto_now=True)



