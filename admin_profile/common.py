from django.db import connection
from django.contrib.auth.models import auth, User, Group, Permission
from admin_profile.models       import Groupinfo


class Common:

	this_group_login_url = '' # admin login url = '' 
	# We can manually update the admin group id if changed in group database table
	this_group_id  = 1 # Admin group id = 1. It can be 4 because both admin and superadmin type users are backend users
	allowed_admin_group_ids = [1,4]

	@classmethod
	def update_this_group_login_url(cls):
		# Getting the dashboard url of admin user group
		group_info               = Groupinfo.objects.filter(group_id=cls.this_group_id).values('description', 'dashboard_url','login_url')
		cls.this_group_login_url = group_info[0]['login_url']

	# constructor to initialize the connection variable
	def __init__(self, connection):
		self.connection = connection
		self.update_this_group_login_url()

	def current_user_group_data(self, logged_in_user_id):

		# group_data = Group.objects.filter(user_id=logged_in_user_id).values('group_id')
		# Fetching the current user group data
		cursor = self.connection.cursor()
		sql    = "SELECT * FROM auth_user_groups WHERE user_id = "+str(logged_in_user_id)+" LIMIT 1 " 
		cursor.execute(sql)
		current_user_group    = cursor.fetchone()
		current_user_group_id = current_user_group[2]
		return current_user_group_id

	def check_user_group(self, user):

		    # If user is authenticated then redirect to their dashboard( According to group )
			logged_in_user_id = user.id
			current_user_group_id = self.current_user_group_data(logged_in_user_id)

			# Return True if its group is in Admin type users else return False
			if current_user_group_id in self.allowed_admin_group_ids:
				return True
			else:
				return False


	# custom method to redirect user to their dashboard 
	# We are using this method in admin login get and post view functions
	def redirect_to_dashboard(self, request):
		# If user is authenticated then redirect to their dashboard( According to group )
		logged_in_user_id = request.user.id
		current_user_group_id = self.current_user_group_data(logged_in_user_id)

		# Getting the dashboard url of logged in user group
		group_info    = Groupinfo.objects.filter(group_id=current_user_group_id).values('description', 'dashboard_url')
		return group_info[0]['dashboard_url']





# -----------------------------------------------------------------------------------------

# admin_login_url = '/backend/'

# #  function to check if logged in user belongs to a specific group(role)
# #  function for user_passes_test decorator which performs a redirect when the callable returns False  
# def check_user_group(user):

# 	admin_group_id = 1
#     # If user is authenticated then redirect to their dashboard( According to group )
# 	logged_in_user_id = user.id

# 	# group_data = Group.objects.filter(user_id=logged_in_user_id).values('group_id')
# 	# Fetching the current user group data
# 	cursor = connection.cursor()
# 	sql    = "SELECT * FROM auth_user_groups WHERE user_id = "+str(logged_in_user_id)+" LIMIT 1 " 
# 	cursor.execute(sql)
# 	current_user_group    = cursor.fetchone()
# 	current_user_group_id = current_user_group[2]

# 	# Return True if its group is Admin else return False
# 	if current_user_group_id == admin_group_id:
# 		return True
# 	else:
# 		return False


# # custom function to redirect user to their dashboard
# def redirect_to_dashboard(request):
# 	# If user is authenticated then redirect to their dashboard( According to group )
# 	logged_in_user_id = request.user.id

# 	# group_data = Group.objects.filter(user_id=logged_in_user_id).values('group_id')
# 	# Fetching the current user group data
# 	cursor = connection.cursor()
# 	sql    = "SELECT * FROM auth_user_groups WHERE user_id = "+str(logged_in_user_id)+" LIMIT 1 " 
# 	cursor.execute(sql)
# 	current_user_group    = cursor.fetchone()
# 	current_user_group_id = current_user_group[2]

# 	# Getting the dashboard url of logged in user group
# 	group_info    = Groupinfo.objects.filter(group_id=current_user_group_id).values('description', 'dashboard_url')
# 	return group_info[0]['dashboard_url']
