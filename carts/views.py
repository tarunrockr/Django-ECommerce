from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from store.models import Product
from .models import Cart, CartItem, CustomerAddress
from orders.models import Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
import ast
from django.contrib.auth.decorators import login_required, user_passes_test
from profiles import common
from django.db import connection



# Common class object
common_obj = common.Common(connection)


import stripe
from django.conf import settings 

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def show_cart(request):

	if request.user.is_authenticated:
		#Fetching cart items from DB
		user_id = request.session['user_id']

		try:
			cart =  Cart.objects.get(user_id = user_id)
		except Cart.DoesNotExist:
			cart = None
			
		if cart is not None:

			try: 
				cart_items = CartItem.objects.select_related('product').filter(cart_id = cart.id).values('id','quantity','product_total','product_id','product__name','product__price')
			except CartItem.DoesNotExist:
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

				#print(cartdata)
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
			#print("Cart: ",len(cart))
			if( len(cart) > 0 ):
				# Total quantity in cart
				total_item = 0
				total = 0
				for key, value in cart.items():
					total_item += value['product_quantity']
					total += value['product_total']

				context = {'success':True, 'message': '', 'cart': cart, 'total_item':total_item, 'total':total, 'source': 'cookie'}
			else:
				context = {'success':False, 'message': 'Your cart is empty.', 'cart': cart,'total_item':0, 'total':0, 'source': 'cookie'}

		else:
			cart= {}
			context = {'success':False, 'message': 'Your cart is empty.', 'cart': cart,'total_item':0, 'total':0, 'source': 'cookie'}

	# print(context)
	# return HttpResponse(context)

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
		user_id = request.session['user_id']

		# Fetching the cart
		try:
			cart = Cart.objects.get(user_id=user_id)
		except cart.DoesNotExist:
			cart = None

		if cart is not None:
			# Fetching the cart
			try:
				cartitem = CartItem.objects.filter(cart_id = cart.id)
			except cartitem.DoesNotExist:
				# Delete the cart
				cart.delete()
				cartitem = None

			if cartitem is not None:

				# Delete the item from cart
				delitem = CartItem.objects.get(product_id=product_id)
				delitem.delete()

				new_total=0.00
				total_item = 0
				if CartItem.objects.filter(cart_id = cart.id).exists():
					reload_status = False
					# Update the cart total amount
					newitems = CartItem.objects.filter(cart_id=cart.id)
					
					for item in newitems:
						total_item += int(item.quantity)
						new_total += float(item.product_total)

					cart.total = new_total
					cart.save()

				else:
					# Delete the cart
					cart.delete()
					reload_status = True

				cartdata = [{'success': True,'error': True, 'message': 'Product removed from cart','total':new_total,'total_item':total_item,'reload': reload_status }]

			else:
				cartdata = [{'success': False,'error': True, 'message': 'Cart is empty', 'total': 0.00,'total_item': 0, 'reload': True}]

		else:
			cartdata = [{'success': False,'error': True, 'message': 'Cart is empty', 'total': 0.00,'total_item': 0, 'reload': True }]

		return JsonResponse(cartdata, safe=False)

	else:
		if 'cart' in request.COOKIES.keys():

			cookie_data = request.COOKIES['cart']
			# using ast.literal_eval() convert dictionary string to dictionary
			cookie_data = ast.literal_eval(cookie_data)

			# Removing the product from cart using "my_dict.pop('key', None)" OR "del my_dict['key']"
			cookie_data.pop(int(product_id), None)
			# del cookie_data[product_id]

			total_item = 0
			total = 0
			if len(cookie_data) == 0 :
				reload = True
			else:
				# Total quantity in cart
				for key, value in cookie_data.items():
					total_item += value['product_quantity']
					total += round(value['product_total'],2)
				reload = False

			data = [{'success': True,'error': False, 'message': 'Product removed from cart', 'total': total, 'total_item': total_item, 'reload': reload}]
			response =  JsonResponse(data, safe=False)
			response.set_cookie('cart', cookie_data)
			return response
		else:
			data = [{'success': False,'error': True, 'message': 'Cart is empty', 'total': 0.00, 'total_item': 0, 'reload': False}]
			return JsonResponse(data, safe=False)


def add_cart_quantity(request):

	product_id = request.POST['product_id']

	if request.user.is_authenticated:
		
		user_id = request.session['user_id']

		# Fetching the cart
		try:
			cart = Cart.objects.get(user_id=user_id)
		except Cart.DoesNotExist:
			cart = None


		if cart is not None:

			try:
				cartitem = CartItem.objects.get(cart_id=cart.id, product_id=product_id)
			except CartItem.DoesNotExist:
				cartitem = None

			if cartitem is not None:

				# Fetch product data
				try:
					product_data = Product.objects.get(pk = product_id)
				except Product.DoesNotExist:
					product_data = None

				if product_data is not None:

					# Updating the cart after increasing the quantity
					cartitem.quantity = int(cartitem.quantity + 1)
					cartitem.product_total = float(cartitem.quantity * product_data.price )
					cartitem.save()

					# Calculate grand total 
					cartitems = CartItem.objects.filter(cart_id=cart.id)
					grand_total = 0.00

					for ele in cartitems:
						grand_total += float(ele.product_total)

					# update cart 
					cart.total = float(grand_total)
					cart.save()

					sub_dict = {'product_quantity': cartitem.quantity, 'product_total': cartitem.product_total}

					data=[{'success': True, 'error': False, 'message': 'Quantity Increased successfully!', 'data': sub_dict,'grand_total': grand_total}]
					return JsonResponse(data, safe=False)

				else:

					data=[{'success': False, 'error': True, 'message': 'Product not exist'}]
					return JsonResponse(data, safe=False)

			else:
				data=[{'success': False, 'error': True, 'message': 'Product not found in cart'}]
				return JsonResponse(data, safe=False)

		else:
			data=[{'success': False, 'error': True, 'message': 'Cart is empty'}]
			return JsonResponse(data, safe=False)


	else:
		if 'cart' in request.COOKIES.keys():

			cookie_data = request.COOKIES['cart']
			# using ast.literal_eval() convert dictionary string to dictionary
			cookie_data = ast.literal_eval(cookie_data)

			sub_dict = None
			for key, value in cookie_data.items():
				if str(key) == str(product_id):
					sub_dict = value


			if sub_dict is not None:

				sub_dict['product_quantity'] += 1
				product_total = sub_dict['product_price'] * sub_dict['product_quantity']
				sub_dict['product_total'] = product_total
				cookie_data[int(product_id)] = sub_dict

				grand_total = 0.00
				for key, value in cookie_data.items():
					grand_total += float(value['product_total'])


				data=[{'success': True, 'error': False, 'message': 'Quantity Increased successfully!', 'data': sub_dict,'grand_total': grand_total}]
				response = JsonResponse(data, safe=False)
				response.set_cookie('cart',cookie_data)
				return response

			else:
				data=[{'success': False, 'error': True, 'message': 'Product not found'}]
				return JsonResponse(data, safe=False)
			

		else:
			data=[{'success': False, 'error': True, 'message': 'Cart is empty'}]
			return JsonResponse(data, safe=False)
		
		

def remove_cart_quantity(request):
	product_id = request.POST['product_id']

	if request.user.is_authenticated:
			
		user_id = request.session['user_id']

		# Fetching the cart
		try:
			cart = Cart.objects.get(user_id=user_id)
		except Cart.DoesNotExist:
			cart = None


		if cart is not None:

			try:
				cartitem = CartItem.objects.get(cart_id=cart.id, product_id=product_id)
			except CartItem.DoesNotExist:
				cartitem = None

			if cartitem is not None:

				# Fetch product data
				try:
					product_data = Product.objects.get(pk = product_id)
				except Product.DoesNotExist:
					product_data = None

				if product_data is not None:

					if cartitem.quantity > 1:

						# Updating the cart after increasing the quantity
						cartitem.quantity = int(cartitem.quantity - 1)
						cartitem.product_total = float(cartitem.quantity * product_data.price )
						cartitem.save()

						# Calculate grand total 
						cartitems = CartItem.objects.filter(cart_id=cart.id)
						grand_total = 0.00

						for ele in cartitems:
							grand_total += float(ele.product_total)

						# update cart 
						cart.total = float(grand_total)
						cart.save()

						sub_dict = {'product_quantity': cartitem.quantity, 'product_total': cartitem.product_total}

						data=[{'success': True, 'error': False, 'message': 'Quantity Decreased successfully!', 'data': sub_dict,'grand_total': grand_total}]
						return JsonResponse(data, safe=False)

					else:

						data=[{'success': True, 'error': False, 'message': 'Mininum 1 quantity required!', 'data': sub_dict,'grand_total': grand_total}]
						return JsonResponse(data, safe=False)
				else:

					data=[{'success': False, 'error': True, 'message': 'Product not exist'}]
					return JsonResponse(data, safe=False)

			else:
				data=[{'success': False, 'error': True, 'message': 'Product not found in cart'}]
				return JsonResponse(data, safe=False)

		else:
			data=[{'success': False, 'error': True, 'message': 'Cart is empty'}]
			return JsonResponse(data, safe=False)

	else:
		if 'cart' in request.COOKIES.keys():

			cookie_data = request.COOKIES['cart']
			# using ast.literal_eval() convert dictionary string to dictionary
			cookie_data = ast.literal_eval(cookie_data)

			sub_dict = None
			for key, value in cookie_data.items():
				if str(key) == str(product_id):
					sub_dict = value


			if sub_dict is not None:

				if sub_dict['product_quantity'] > 1:

					sub_dict['product_quantity'] -= 1
					product_total = sub_dict['product_price'] * sub_dict['product_quantity']
					sub_dict['product_total'] = product_total
					cookie_data[int(product_id)] = sub_dict

					grand_total = 0.00
					for key, value in cookie_data.items():
						grand_total += float(value['product_total'])


					data=[{'success': True, 'error': False, 'message': 'Quantity Decreased successfully!', 'data': sub_dict,'grand_total': grand_total}]
					response = JsonResponse(data, safe=False)
					response.set_cookie('cart',cookie_data)
					return response

				else:

					data=[{'success': False, 'error': True, 'message': 'Minimum 1 quantity required'}]
					return JsonResponse(data, safe=False)

			else:
				data=[{'success': False, 'error': True, 'message': 'Product not found'}]
				return JsonResponse(data, safe=False)
			
		else:
			data=[{'success': False, 'error': True, 'message': 'Cart is empty'}]
			return JsonResponse(data, safe=False)

def checkout_login_check(request):
	

	if request.user.is_authenticated:
		data = [{'login': True}]
		return JsonResponse(data, safe=False)
	else:
		data = [{'login': False}]
		return JsonResponse(data, safe=False)

# Checkout page functions 

# Show checkout page
@login_required( login_url = common_obj.this_group_login_url )
@user_passes_test( common_obj.check_user_group, login_url = common_obj.this_group_login_url )
def checkout(request):

	if request.user.is_authenticated:

		user_id = request.session['user_id']
		#Fetch cart data
		cart_data = Cart.objects.get(user_id=user_id)

		STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY
		return render(request,"front/checkout/checkout.html",{'cart_data': cart_data, 'user_id': user_id, 'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY })

def create_checkout_session(request):

	#Fetch total amount
	user_id = request.session['user_id']
	#Fetch cart data
	cart_data = Cart.objects.get(user_id=user_id)

	# we can give any custome information in metadata  

	YOUR_DOMAIN = 'http://127.0.0.1:8000/'
	checkout_session = stripe.checkout.Session.create(
	    payment_method_types=['card'],
	    line_items=[
	        {
	            'price_data': {
	                'currency': 'usd',
	                'unit_amount': (int(cart_data.total)*100),
	                'product_data': {
	                    'name': 'Stubborn Attachments',
	                    # 'images': ['https://i.imgur.com/EHyR2nP.png'],
	                },
	            },
	            'quantity': 1,
	        },
	    ],
	    metadata={
	    	'cart_id': cart_data.id,
	    	'user_id': user_id
	    },
	    mode='payment',
	    success_url=YOUR_DOMAIN + 'checkout_success',
	    cancel_url=YOUR_DOMAIN + 'checkout_success',
	)

	return JsonResponse({ 'id': checkout_session.id })

def checkout_post(request):
	return HttpResponse("In checkout post")

def checkout_success(request):
	return render(request, 'front/checkout/success.html', {})

def checkout_cancel(request):
	return render(request, 'front/checkout/cancel.html', {})

@csrf_exempt
def stripe_webhook(request):
  	payload = request.body
  	sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  	event = None

  	try:
  		event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
  	except ValueError as e:
  		# Invalid payload
  		return HttpResponse(status=400)
  	except stripe.error.SignatureVerificationError as e:
  		# Invalid signature
  		return HttpResponse(status=400)

  	# Handle the checkout.session.completed event
  	if event['type'] == 'checkout.session.completed':
  		stripe_session = event['data']['object']

  		# Fulfill the purchase...
  		order_status = save_order(stripe_session)
  		print(stripe_session)

  	# Passed signature verification
  	return HttpResponse(status=200)

def save_order(stripe_response):

	# print("Fulfilling order")
	transaction_id = stripe_response.id
	user_id        = stripe_response.metadata.user_id
	cart_id        = stripe_response.metadata.cart_id

	# Fetch all record of cart
	try:
		cart_data = Cart.objects.get(id=cart_id)
	except Cart.DoesNotExist:
		cart_data = None

	if cart_data is not None:

		# Insert into orders table
		order = Order(user_id=user_id, total=cart_data.total, transaction_id=transaction_id)
		order.save()
		latest_order_id = Order.objects.latest('id')
		# Fetch all record of cart items
		try:
			cart_items = CartItem.objects.filter(cart_id=cart_data.id)
		except CartItem.DoesNotExist:
			cart_items = None

		if cart_items is not None:
			# Insert into order detail table
			for data in cart_items:
				product_info = Product.objects.get(id=data.product_id)
				order_item = OrderItem(order_id=latest_order_id.pk, product_id=data.product_id, quantity=data.quantity, product_price=product_info.price, product_total=data.product_total)
				order_item.save()

		# Removing the current cart and its item data
		cart_data.delete()
		cart_items.delete()

	return True


def	add_shipping_address_ajax(request):

	if request.user.is_authenticated:

		
		user_list = request.POST['form_data'].split("&")
		user_dict = {}
		for ele in user_list:
			user_dict[ele.split("=")[0]] = ele.split("=")[1]

		user_id        = request.session['user_id']
		first_name     = user_dict['first_name']
		last_name      = user_dict['last_name']
		email          = user_dict['email']
		mobile         = int(user_dict['mobile'])
		address_line_1 = user_dict['address_line_1']
		address_line_2 = user_dict['address_line_2'] if 'address_line_2' in user_dict else ''
		country        = user_dict['country']
		state          = user_dict['state']
		postcode       = user_dict['postcode']

		customer_address = CustomerAddress(user_id=user_id, first_name=first_name, last_name=last_name, email=email, mobile=mobile, address_line1=address_line_1, address_line2=address_line_2, country=country, state=state, postcode=postcode, is_shipping=1)
		customer_address.save()
		#last_insert_id = CustomerAddress.objects.latest('id')
		data = [{'success': True, 'message': "Address added successfully", 'login': True, 'data': ''}]
		return JsonResponse(data, safe=False)

	else:

		data = [{'success': False, 'message': "Please login to continue", 'login': False}]
		return JsonResponse(data, safe=False)


def fetch_shipping_address_ajax(request):

	if request.user.is_authenticated:

		user_id = request.POST['user_id']

		# Fetch existing shipping address
		all_address = CustomerAddress.objects.filter(user_id=user_id, is_shipping=1)
		address='';
		if all_address:
			for add in all_address:
				
				if add.is_default_shipping == 1:
					checked = 'checked'
				else:
					checked = ''

				address += '<div class="card-new bg-light mb-3">'
				address += ' <div class="card-body">'
				address += f'  <h5 class="card-title">Name: {add.first_name} {add.last_name}  | <label>Select: <input type="radio" name="select_address_id" id="select_address_id" {checked} class="select_address_radio" value="{add.id}"></label></h5>'
				
				address += '   <div class="row">'
				address += '    <div class="col-md-6">'
				address += '	 <label><b>Email:</b></label>'
				address += f'     <span>{add.email}</span>'
				address += '    </div>'
				address += '    <div class="col-md-6">'
				address += '     <label><b>Mobile:</b></label>'
				address += f'     <span>{add.mobile}</span>'
				address += '    </div>'
				address += '   </div>'

				address += '   <div class="row">'
				address += '    <div class="col-md-3">'
				address += '	 <label><b>Address Line 2:</b></label>'
				address += '    </div>'
				address += '    <div class="col-md-9">'
				address += f'     <span>{add.address_line1}</span>'
				address += '    </div>'
				address += '   </div>'

				address += '   <div class="row">'
				address += '    <div class="col-md-3">'
				address += '	 <label><b>Address Line 2:</b></label>'
				address += '    </div>'
				address += '    <div class="col-md-9">'
				address += f'     <span>{add.address_line2}</span>'
				address += '    </div>'
				address += '   </div>'

				address += '   <div class="row">'
				address += '    <div class="col-md-4">'
				address += '	 <label><b>Country:</b></label>'
				address += f'     <span>{add.country}</span>'
				address += '    </div>'
				address += '    <div class="col-md-4">'
				address += '     <label><b>State:</b></label>'
				address += f'     <span>{add.state}</span>'
				address += '    </div>'
				address += '    <div class="col-md-4">'
				address += '     <label><b>Postcode:</b></label>'
				address += f'     <span>{add.postcode}</span>'
				address += '    </div>'
				address += '   </div>'

				address += ' </div>'
				address += '</div>'
		else:
			address += '<div class="card-new bg-light mb-3">'
			address += ' <div class="card-body">'

			address += '   <div class="row">'
			address += '    <div class="col-md-12">'
			address += '     <div class="alert alert-info" role="alert">'
			address += '     	Address is not available  <a href="#" class="alert-link">Add new address.</a>'
			address += '     </div>'
			address += '    </div>'
			address += '   </div>'

			address += ' </div>'
			address += '</div>'

		# serialized_obj = serializers.serialize('json', all_address)

		data = [{'success': True, 'message': 'in function', 'login': True,'data': address}]
		return JsonResponse(data, safe=False)
	else:
		data = [{'success': True, 'message': 'Please login to continue', 'login': False}]
		return JsonResponse(data, safe=False)


def update_cart_logo_count(request):

	if request.user.is_authenticated:

		user_id = request.session['user_id']
		cart_count = 0
		try:
			cart_data     = Cart.objects.get(user_id = user_id)
		except Cart.DoesNotExist:
			cart_data = None
		if cart_data is not None:
			try:
				cartitem_data = CartItem.objects.filter(cart_id = cart_data.id)
			except CartItem.DoesNotExist:
				cartitem_data = None

			if cartitem_data is not None:
				for ele in cartitem_data:
					cart_count +=  ele.quantity

		data = [{'cart_count': cart_count}]
		return JsonResponse(data, safe=False)

	else:
		# Getting the cart item count from cookies
		if 'cart' in request.COOKIES.keys():

			# Get cart from cookies
			data = request.COOKIES['cart']

			# using ast.literal_eval() convert dictionary string to dictionary
			data = ast.literal_eval(data)

			total_item = 0

			for key, value in data.items():
				total_item += value['product_quantity']

			data = [{'cart_count': cart_count}]
			return JsonResponse(data, safe=False)

		else:

			data = [{'cart_count': cart_count}]
			return JsonResponse(data, safe=False)

	

