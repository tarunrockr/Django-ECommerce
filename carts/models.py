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