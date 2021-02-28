from django.shortcuts import render

# Create your views here.

def register_show(request):
	
	return render(request, 'front/profiles/register.html', {})

def register_post(request):
	pass
	# render(request, '', {})

def login_show(request):
	pass
	# render(request, '', {})

def login_post(request):
	pass
	# render(request, '', {})
