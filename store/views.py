from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# Create your views here.

def index(request):

	product_data = Product.objects.all()
	return render(request, 'front/index.html', {'product_data': product_data})
