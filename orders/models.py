from django.db import models
from django.contrib.auth.models import User
from store.models import Product
# Create your models here.

# Order table
class Order(models.Model):
	user       = models.ForeignKey(User, null=True, blank=True, on_delete = models.CASCADE)
	total      = models.DecimalField(max_digits=50, decimal_places=2, null=True, default=0.00)
	billing_address_id  = models.IntegerField(null=True)
	shipping_address_id = models.IntegerField(null=True)
	transaction_id      = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
	status     = models.IntegerField(default=1)

	def __str__(self):
		return self.total


# Order detail table
class OrderItem(models.Model):
	
	order 		  = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE)
	product 	  = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
	quantity 	  = models.IntegerField(blank=True, default=1)
	product_price = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	product_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	created_at    = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at    = models.DateTimeField(auto_now_add=False, auto_now=True)
	status        = models.IntegerField(default=1)

	def __str__(self):
		return  self.product.name








