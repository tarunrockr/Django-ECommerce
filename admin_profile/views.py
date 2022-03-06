from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import TestStudent, Dummy

# Create your views here.


def dashboard(request):
	# return HttpResponse('In admin dashboard')
	print("In dashboard")
	return render(request, 'admin/profiles/dashboard.html')



# Test functions

def test_function(request):
	# student_data = TestStudent.objects.all()
	student_data = TestStudent.students.get_stu_roll_range(102,105)

	# ORM Test functions

	# usr = Dummy.objects.all()

	# usr = Dummy.objects.filter(name__exact="tarun")
	# usr = Dummy.objects.filter(name__iexact="tarun")
	# usr = Dummy.objects.filter(name__contains="i")
	# usr = Dummy.objects.filter(name__icontains="i")
	# usr = Dummy.objects.filter(id__in=[2,4,6])
	# usr = Dummy.objects.filter(roll__in=[101,104,105])
	# usr = Dummy.objects.filter(marks__gt=30)
	# usr = Dummy.objects.filter(marks__gte=30)
	# usr = Dummy.objects.filter(marks__lt=50)
	# usr = Dummy.objects.filter(marks__lte=50)
	# usr = Dummy.objects.filter(name__startswith='T')
	# usr = Dummy.objects.filter(name__istartswith='T')
	# usr = Dummy.objects.filter(name__endswith='y')
	# usr = Dummy.objects.filter(name__iendswith='y')
	usr = Dummy.objects.filter(passdate__range=('2021-07-01','2021-09-30'))

	print(usr.query)
	return render(request, 'admin/profiles/table.html',{'student':student_data,'usr':usr})