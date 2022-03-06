from django.db import models
from django.contrib.auth.models import User
from store.models import Product
# Create your models here.

# Table for cart according to user
class Cart(models.Model):
	user 		= models.ForeignKey(User, null=True, blank=True, on_delete = models.CASCADE)
	total   	= models.DecimalField(max_digits=50 , decimal_places=2, default=0.00)
	created_at  = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at  = models.DateTimeField(auto_now_add=False, auto_now=True)
	status      = models.IntegerField(default = 1)

	def __str__(self):
		return "Cart ID %s"%(self.id)

#cart detail table
class CartItem(models.Model):
	cart        	= models.ForeignKey(Cart, null=True, blank=True, on_delete = models.CASCADE)
	product         = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
	quantity    	= models.IntegerField(blank=True, default=1)
	product_total	= models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	created_at  	= models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at  	= models.DateTimeField(auto_now_add=False, auto_now=True)
	status      	= models.IntegerField(default = 1)

	def __str__(self):
		return self.product.name


# Address table
class CustomerAddress(models.Model):

	user          = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	first_name    = models.CharField(max_length=200, null=True, blank=True)
	last_name     = models.CharField(max_length=200, null=True, blank=True)
	email         = models.CharField(max_length=100, null=True, blank=True)
	mobile        = models.CharField(max_length=100, null=True, blank=True)
	address_line1 = models.TextField(null=True)
	address_line2 = models.TextField(null=True)
	country       = models.CharField(max_length=100, null=True, blank=True)
	state         = models.CharField(max_length=100, null=True, blank=True)
	postcode      = models.CharField(max_length=50, null=True, blank=True)
	is_billing    = models.IntegerField(default=0)
	is_shipping   = models.IntegerField(default=0)
	is_default_shipping   = models.IntegerField(default=0)
	status        = models.IntegerField(default=1)
	created_at    = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at    = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):

		return self.first_name


