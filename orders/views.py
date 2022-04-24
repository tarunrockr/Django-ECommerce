from   django.shortcuts import render
from   django.db import connection
from   django.http import HttpResponse, JsonResponse
from   django.utils import formats
import json
import pprint
from django.contrib.auth.decorators import login_required, user_passes_test
from profiles import common
from django.db import connection



# Common class object
common_obj = common.Common(connection)


@login_required( login_url = common_obj.this_group_login_url )
@user_passes_test( common_obj.check_user_group, login_url = common_obj.this_group_login_url )
def order_list(request):
	return render(request, 'front/orders/orders.html', {})


# Server side data table code , START

DEFAULT_START_POSITION = 0
DEFAULT_PAGE_SIZE = 10
DEFAULT_SORTING_COLUMN_INDEX = 1
DEFAULT_SORTING_METHOD = 'asc'

#constants for querying
# ORDER_DICT = {
#     0: 'field1',
#     1: 'field2',
# }

# ORDER_BY = {
#     'desc': '-',
#     'asc': ''
# }

# QUERY_FIELDS = ['field1', 'field2']

# def get_sorting(self, request_values):
#     return int(request_values.get('iSortCol_0', self.DEFAULT_SORTING_COLUMN_INDEX)),\
#            request_values.get('sSortDir_0', self.DEFAULT_SORTING_METHOD).lower()

# def get_paging(self, request_values):
#     return int(request_values.get('iDisplayStart', self.DEFAULT_START_POSITION)),\
#                int(request_values.get('iDisplayLength', self.DEFAULT_PAGE_SIZE))


@login_required( login_url = common_obj.this_group_login_url )
@user_passes_test( common_obj.check_user_group, login_url = common_obj.this_group_login_url )
def orders_data_ajax(request):

	#pprint.pprint(request.GET)
	cursor = connection.cursor()

	# Set default parameters 
	DEFAULT_START_POSITION       = 0
	DEFAULT_PAGE_SIZE            = 10
	DEFAULT_SORTING_COLUMN_INDEX = 1
	DEFAULT_SORTING_METHOD       = 'desc'
	
	# ... receive the request

	# paging
	# start       = request.GET.get('iDisplayStart', DEFAULT_START_POSITION)    # Offset
	start       = request.GET.get('start', DEFAULT_START_POSITION)    # Offset
	#length      = request.GET.get('iDisplayLength', DEFAULT_PAGE_SIZE)        # Length
	length      = request.GET.get('length', DEFAULT_PAGE_SIZE)        # Length
	# sorting
	# sort_column = request.GET.get('iSortCol_0', DEFAULT_SORTING_COLUMN_INDEX) # Default column for sorting
	sort_column = request.GET.get('order[0][column]', DEFAULT_SORTING_COLUMN_INDEX) # Default column for sorting
	# sort_type   = request.GET.get('sSortDir_0', DEFAULT_SORTING_METHOD)       # Sort type 'asc' or 'desc'
	sort_type   = request.GET.get('order[0][dir]', DEFAULT_SORTING_METHOD)       # Sort type 'asc' or 'desc'
	# research query
	# search_keyword= request.GET.get('sSearch', '')                              # Search String
	search_keyword= request.GET.get('search[value]', '')                              # Search String
	where = ''
	inc = 0

	# Database column number to table column name mapping
	arr = {
		0: "t1.id",
		1: "t1.total",
		2: "t1.created_at"
	}

	# Map the sorting column index to the column name
	sort_by = arr[int(sort_column)]
	if sort_by == "":
		sort_by = "t1.id"

	# research sql
	if search_keyword != '':
		where = " WHERE (t1.total LIKE('%"+search_keyword+"%') ) "

	# Get the records after applying the database filters
	datasql = "SELECT t1.id , t1.total, t1.created_at FROM orders_order as t1 "+where+" ORDER BY "+sort_by+" "+sort_type+" LIMIT  "+str(start)+" , "+str(length)+"  "
	print("query: ",datasql)
	cursor.execute(datasql)
	all_data = cursor.fetchall()
	all_data = list(all_data)

	# Get the total record count without any condition to maintain pagination
	countsql = "SELECT t1.id , t1.total, t1.created_at FROM orders_order as t1 "+where+" "
	cursor.execute(countsql)
	count_data = cursor.fetchall()
	count = len(list(count_data)) # Total rows in queryset

	# json dict to be returned
	records = {
    	'iTotalRecords': count,    # The total count of records in your database, if query exist, it is the count of filtered records
        'iTotalDisplayRecords': count,    # Represents the rendering count of datatable
        'aaData': [],    # Main data to be rendered in table
    }

    # if no query, all records returned
    # records.update({'iTotalDisplayRecords': count if search_keyword else records['iTotalRecords']})
    
	if(all_data):
		for data in all_data:
			# dict1 = { "id": (inc + 1), "total": float(data[1]), "created_at": formats.date_format(data[2], "SHORT_DATETIME_FORMAT") }
			action_data = "<a href='#' class='btn-sm btn-primary' title='View Order Details'><i class='fa fa-eye'></></a>"
			dict1 = { 
						"id": (inc + 1), 
						"total": float("{:.2f}".format(data[1])), 
						"created_at": data[2].strftime("%d-%m-%Y %I:%M:%S %p"),
						"actions":  action_data,
					}
			records['aaData'].append(dict1)
			inc += 1

	return HttpResponse(json.dumps(records), content_type='application/json')
	# return JsonResponse(records, safe=False)







# Server side data table code , END