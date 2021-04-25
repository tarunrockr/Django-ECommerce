import ast
from carts.models import Cart, CartItem


def cart_item_count(request):

	if request.user.is_authenticated:

		user_id = request.session['user_id']
		cart_count = 0
		try:
			cart_data     = Cart.objects.get(user_id = user_id)
		except:
			cart_data = None
		if cart_data is not None:
			try:
				cartitem_data = CartItem.objects.filter(cart_id = cart_data.id)
			except:
				cartitem_data = None

		if cartitem_data is not None:
			for ele in cartitem_data:
				cart_count +=  ele.quantity

		return {
			'cart_count': cart_count
		}

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

			return {
				'cart_count': total_item
			}

		else:

			return {
				'cart_count': 0
			}
