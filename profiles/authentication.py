from django.contrib.auth.models import User, auth, Group, Permission
from django.contrib.auth.backends import ModelBackend
from django.db import connection

from django.db.models import Q

class EmailAuthBackend(ModelBackend):
    """
        Authenticate using e-mail account
    """
    def authenticate(self, request, email=None, password=None, login_type=None, **kwars):

        try:
            print("Login Type: ",login_type)
            if(login_type == 'backend'):
                user = User.objects.get(email=email)

                # Fetching all the groups except 'customer' group
                groups = Group.objects.filter(~Q(name='customer')).values('id','name')
                group_list = [ ele['id'] for ele in groups ]
                print("Group list ",group_list)
                # Fetching current user group
                cursor = connection.cursor()
                sql = "SELECT * FROM auth_user_groups WHERE user_id = "+str(user.id)+" LIMIT 1"
                cursor.execute(sql)
                current_user_group = cursor.fetchone()
                current_user_group_id = current_user_group[2]

                print(current_user_group_id)

                # Allowed groups to login from backend(admin, superadmin)
                allowed_admin_group_ids = [1,4]
                
                if current_user_group_id in group_list:
                    if current_user_group_id in allowed_admin_group_ids:
                        if user.check_password(password):
                            return user

                return None
                
            elif(login_type == 'frontend'):
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return user

                return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
