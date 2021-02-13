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
	brand        = models.CharField(max_length=250, null=True)
	category     = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	ram          = models.IntegerField(null=True)
	storage      = models.IntegerField(null=True)
	camera       = models.CharField(max_length=200, null=True)
	quantity     = models.IntegerField(null=True)
	description  = models.CharField(max_length=255, default='', null=True, blank=True)
	image        = models.ImageField(upload_to='upload/products/')
	status       = models.IntegerField(default='1')
	created_at   = models.DateTimeField(auto_now_add=True)
	updated_at   = models.DateTimeField(auto_now=True)



