from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
import ast

# Create your views here.

def show_cart(request):

	if request.user.is_authenticated:
		#Fetching cart items from DB
		user_id = request.session['user_id']

		try:
			cart =  Cart.objects.get(user_id = user_id)
		except cart.DoesNotExist:
			cart = None

			
		if cart is not None:

			try: 
				cart_items = CartItem.objects.select_related('product').filter(cart_id = cart.id).values('id','quantity','product_total','product_id','product__name','product__price')
			except cart_items.DoesNotExist:
				cart_items = None

			if cart_items is not None:

				# print(cart_items)
				# print(cart_items.query)
				cartdata = dict()
				total_item = 0
				total = 0
				if cart_items:
					for ele in cart_items:
						total_item += ele['quantity']
						total += float(ele['product_total']) 
						cartdata[ele['product_id']] = {'product_name': ele['product__name'],'product_quantity': ele['quantity'], 'product_price': float(ele['product__price']), 'product_total': float(ele['product_total']) }

				print(cartdata)
				#return HttpResponse(cartdata)
				context = {'success':True, 'message': '', 'cart': cartdata,'total_item':total_item, 'total':total, 'source': 'database'}

			else:
				cartdata = {}
				context = {'success':False, 'message': 'Your cart is empty.', 'cart': cartdata,'total_item':0, 'total':0, 'source': 'database'}

		else:
			cartdata = {}
			context = {'success':False, 'message': 'Your cart is empty.', 'cart': cartdata,'total_item':0, 'total':0, 'source': 'database'}

		return render(request, 'front/carts/cart.html', context)

	else:
		# Fetching the cart items from the cookie
		if 'cart' in request.COOKIES.keys():
			cart = request.COOKIES['cart']
			# using ast.literal_eval() convert dictionary string to dictionary
			cart = ast.literal_eval(cart)
			# Total quantity in cart
			total_item = 0
			total = 0
			for key, value in cart.items():
				total_item += value['product_quantity']
				total += value['product_total']

			context = {'success':True, 'message': '', 'cart': cart, 'total_item':total_item, 'total':total, 'source': 'cookie'}
		else:
			cart= {}
			context = {'success':False, 'message': 'Your cart is empty.', 'cart': cart,'total_item':0, 'total':0, 'source': 'cookie'}

	return render(request, 'front/carts/cart.html', context)


def update_cart(request):

	product_id = request.POST.get('product_id', False)

	if request.user.is_authenticated: # Fetching the product data from the cart from database when logged in

		# Fetch product details
		try:
			product = Product.objects.get(pk=product_id)
		except product.DoesNotExist:
			data =[{'success': False,'error': True, 'message': 'Product not found.'}]
			return JsonResponse(data)

		user_id = request.user.id
		cartID = 0
		try:
			cart = Cart.objects.get(user_id= user_id)
			cartID   = cart.pk 
		except:
			cart = None

		if cart is None:

			# Adding record to cart table
			cart 		 =  Cart()
			cart.user_id =  user_id
			cart.save()

			# Get the cart_id 
			cart_id = Cart.objects.latest('id')
			cartID  = cart_id.pk

			# Adding data to cart item
			cartitem   = CartItem.objects.create(quantity=1, product_total=product.price, cart_id=cart_id.pk, product_id=product_id)
			cart.total = product.price
			cart.save()

		else:
			try:
				cartitem = CartItem.objects.get(cart_id=cart.pk, product_id=int(product_id))
			except:
				cartitem = None

			if cartitem is not None:
				cartitem.quantity 		= cartitem.quantity + 1
				cartitem.product_total	= cartitem.quantity * product.price
				cartitem.save()

			else:
				# Adding data to cart item
				cartitem   = CartItem.objects.create(cart_id=cart.pk, quantity=1, product_total=product.price, product_id=product_id)

		# Updating the cart total value 
		cartitems = CartItem.objects.filter(cart_id=cartID)
		new_total=0.00
		for item in cartitems:
			new_total += float(item.product_total)
		cart.total = new_total
		cart.save()

		data =[{'success': True,'error': False, 'message': 'Product added to cart.'}]
		return JsonResponse(data, safe=False)

	else: # Fetching the product data from the cart from cookie , when not logged in 

		# Fetch product details
		try:
			product = Product.objects.get(pk=product_id)
		except Product.DoesNotExist:
			product = None

		# serialized_obj = serializers.serialize('json', [ product, ])
		# data =[{'User is not logged in ':serialized_obj}]
		# return JsonResponse(data, safe=False)

		if product is not None:

			max_age_time = 365 * 24 * 60 * 60  # one year
			if 'cart' in request.COOKIES.keys():

				data = request.COOKIES['cart']

				# # using json.loads() to convert dictionary string to dictionary
				# result = json.loads(data)
				# x = result[product.id]['product_name']

				# using ast.literal_eval() convert dictionary string to dictionary
				result = ast.literal_eval(data)

				if product.id in result:
					# If key exists in dictionary , then update quantity and product total
					result[product.id]['product_quantity'] += 1
					result[product.id]['product_total'] = result[product.id]['product_quantity'] * float(result[product.id]['product_price']) 
					# json_data = json.dumps(result[product.id])
					data =[{'success': False,'error': True, 'message': 'exist and updated' }]
					response =  JsonResponse(data, safe=False)
					response.set_cookie('cart', result, max_age=max_age_time)
					return response

				else:
					# If key not exists in dictionary , then add product as new sub dictionary and product id as key
					product_dict = {'product_name': product.name, 'product_quantity': 1, 'product_price': product.price, 'product_total': product.price}
					result[product.id] = product_dict
					data =[{'success': False,'error': True, 'message': 'exist and updated' }]
					response =  JsonResponse(data, safe=False)
					response.set_cookie('cart', result, max_age=max_age_time)
					return response

			else:
				product_dict = {'product_name': product.name, 'product_quantity': 1, 'product_price': product.price, 'product_total': product.price}
				cart_dict    = { product.id:  product_dict}
				# Setting cart in cookie
				data =[{'success': True,'error': False, 'message': 'Product added to cart'}]
				response =  JsonResponse(data, safe=False)
				response.set_cookie('cart', cart_dict, max_age=max_age_time)
				return response
			
		else:
			data =[{'success': False,'error': True, 'message': 'Product added to cart'}]
			return JsonResponse(data, safe=False)


		
def remove_cart_product(request):

	product_id = request.POST['product_id']

	if request.user.is_authenticated:
		pass

	else:
		if 'cart' in request.COOKIES.keys():

			cookie_data = request.COOKIES['cart']
			# using ast.literal_eval() convert dictionary string to dictionary
			cookie_data = ast.literal_eval(cookie_data)

			# Removing the product from cart using "my_dict.pop('key', None)" OR "del my_dict['key']"
			cookie_data.pop(int(product_id), None)
			# del cookie_data[product_id]

			if len(cookie_data) == 0 :
				reload = True
			else:
				reload = False

			data = [{'success': True,'error': False, 'message': 'Product removed from cart', 'reload': reload}]
			response =  JsonResponse(data, safe=False)
			response.set_cookie('cart', cookie_data)
			return response
		else:
			data = [{'success': False,'error': True, 'message': 'Cart is empty','reload': False}]
			return JsonResponse(data, safe=False)

