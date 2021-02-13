from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.db import connection
from django.http import JsonResponse
import os
from django.conf import settings

# Create your views here.

def home(request):

	return render(request, 'front/index.html')

def products(request):

	cursor = connection.cursor()

	product_data = Product.objects.all()

	# Fetch brand
	brandSql= ''' SELECT brand FROM store_product WHERE STATUS =1 GROUP BY brand ORDER BY brand ASC  '''
	cursor.execute(brandSql)
	brand = cursor.fetchall()

	# Fetch ram
	ramSql= ''' SELECT ram FROM store_product WHERE STATUS =1 GROUP BY ram ORDER BY ram ASC  '''
	cursor.execute(ramSql)
	ram = cursor.fetchall()

	# Fetch ram
	storageSql= ''' SELECT storage FROM store_product WHERE STATUS =1 GROUP BY storage ORDER BY storage ASC  '''
	cursor.execute(storageSql)
	storage = cursor.fetchall()

	# Fetch category
	categorySql= ''' SELECT name FROM store_category ORDER BY name ASC '''
	cursor.execute(categorySql)
	category = cursor.fetchall()

	return render(request, 'front/products/products.html', {'product_data': product_data, 'brands': brand, 'rams':ram, 'storages': storage, 'categories': category })


def fetch_products_ajax(request):

	cursor = connection.cursor()
	
	brand   = request.POST.getlist('brand[]')
	ram     = request.POST.getlist('ram[]')
	storage = request.POST.getlist('storage[]')

	sql = "SELECT * FROM store_product WHERE 1"
	
	if brand:
		brand_string = ",".join("'" + item + "'" for item in brand)
		sql += " AND brand IN("+brand_string+")"

	if ram:
		ram_string = ",".join("'" + item + "'" for item in ram)
		sql += " AND ram IN("+ram_string+")"

	if storage:
		storage_string = ",".join("'" + item + "'" for item in storage)
		sql += " AND storage IN("+storage_string+")"

	cursor.execute(sql)
	products = cursor.fetchall()

	output=''
	if products:
		for product in products:

			output+="<div class='col-lg-4 col-md-6 col-sm-10 offset-md-0 offset-sm-1'>"
			output+="<div class='card'> <img class='card-img-top' src='{0}'>".format( os.path.join(settings.MEDIA_URL, product[4]) )
			output+="<div class='card-body'>"

			output+="<h5><b>{0}</b> </h5>".format(product[1])
			output+="<div class='d-flex flex-row my-2'>"
			output+="<div class='text-muted'>Price: {0}₹<br>Brand: {1}<br>Ram: {2} GB<br>Storage: {3} GB<br></div>".format(product[2],product[9].title(),product[12],product[13])
			
			output+="<div class='ml-auto'>"
			output+="<button class='border rounded bg-white sign'><span class='fa fa-minus' id='orange'></span></button>"
			output+="<span class='px-sm-1'>1 item</span>"
			output+="<button class='border rounded bg-white sign'><span class='fa fa-plus' id='orange'></span></button>"
			output+="</div>"

			output+="</div>"
			output+="<button class='btn w-100 rounded my-2'>Add to cart</button>"

			output+="</div>"
			output+="</div>"
			output+="</div>"
			output+="</div>"
	else:
		output += "<div class ='alert alert-warning text-center' style='width: 100%;margin-top: 10%;' ><span style='font-size:25px;'><strong>No result found.</strong></span></div>"


	data = [{'data':output}]
	return JsonResponse(data, safe=False)
