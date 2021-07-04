from django.http import HttpResponse

# Middleware process using the middleware function
# def my_middleware(get_response):

# 	print("One Time Initialization")

# 	def my_function(request):

# 		print("This is before view.")
# 		response = get_response(request)
# 		print("This is after view.")

# 		return response

# 	return my_function

# -----------------------------------------------------------

# Middleware process using the middleware class
# class MyMiddleware:

# 	def __init__(self,get_response):
# 		self.get_response = get_response
# 		print("One Time Initialization")

# 	def __call__(self, request):

# 		print("Before view function in class middleware")
# 		response = self.get_response(request)
# 		print("After view function in class middleware")

# 		return response

# -----------------------------------------------------------

# Multiple middleware in sequence
# Middleware process using the middleware class
# class MyMiddleware1:

# 	def __init__(self,get_response):
# 		self.get_response = get_response
# 		print("One Time Initialization Middle1")

# 	def __call__(self, request):
# 		print("Before view function in class middleware Middle1")
# 		response = self.get_response(request)
# 		print("After view function in class middleware Middle1")
# 		return response

# class MyMiddleware2:

# 	def __init__(self,get_response):
# 		self.get_response = get_response
# 		print("One Time Initialization Middle2")

# 	def __call__(self, request):
# 		print("Before view function in class middleware Middle2")
# 		response = self.get_response(request)
# 		# Here we can redirect to a url if the condition is not met
# 		#response = HttpResponse("Response from middleware 2")
# 		print("After view function in class middleware Middle2")
# 		return response


# class MyMiddleware3:

# 	def __init__(self,get_response):
# 		self.get_response = get_response
# 		print("One Time Initialization Middle3")

# 	def __call__(self, request):
# 		print("Before view function in class middleware Middle3")
# 		response = self.get_response(request)
# 		print("After view function in class middleware Middle3")
# 		return response


# -----------------------------------------------------------

# class MyProcessMiddleware:

# 	def __init__(self,get_response):
# 		self.get_response = get_response
# 		print("One Time Initialization")

# 	def __call__(self, request):

# 		response = self.get_response(request)
# 		return response


# 	def process_view(request, *args, **kwargs):
# 		print("This is process view - Before View")
# 		#return HttpResponse("This is before view")
# 		return None

# -----------------------------------------------------------

# class MyExceptionMiddleware:

# 	def __init__(self,get_response):
# 		self.get_response = get_response
# 		print("One Time Initialization")


# 	def __call__(self, request):
# 		response = self.get_response(request)
# 		return response

# 	def process_exception(self, request, exception):
# 		msg = exception
# 		class_name = exception.__class__.__name__
# 		return HttpResponse(class_name)


# -----------------------------------------------------------

class MyTemplateResponseMiddleware:

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response =  self.get_response(request)
		return response

	def process_template_response(self, request, response):
		print("Process Template Response from Middleware")
		response.context_data['heading_name'] = "Admin Login"
		return response