from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def dashboard(request):
	# return HttpResponse('In admin dashboard')
	print("In dashboard")
	return render(request, 'admin/profiles/dashboard.html')