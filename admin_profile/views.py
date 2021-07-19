from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import TestStudent

# Create your views here.


def dashboard(request):
	# return HttpResponse('In admin dashboard')
	print("In dashboard")
	return render(request, 'admin/profiles/dashboard.html')


def test_function(request):
	student_data = TestStudent.objects.all()
	# student_data = TestStudent.students.all()
	return render(request, 'admin/profiles/table.html',{'student':student_data})