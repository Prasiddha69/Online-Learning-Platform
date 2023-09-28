from django.contrib.auth.backends import ModelBackend

from .models import User

# class RoleBasedAuthenticationBackend(ModelBackend):
#     def authenticate(self,request,username=None,password=None,**kwargs):
#         try:
#             user = User.objects.get(username=username)

#             if user.role == 'teacher' and user.check_password(password):
#                 return user
     
#         except User.DoesNotExist:
#             return None
        
    # def get_user(self,user_id):
    #     try:
    #         return User.objects.get(pk=user_id)
    #     except User.DoesNotExist:
    #         return None


class TeacherBackend(ModelBackend):
    def authenticate(self,request, username=None, password=None,**kwargs):
        try:
            user = User.objects.get(username=username,role="teacher")

            if user.check_password(password):
                return user
     
        except User.DoesNotExist:
            return None
    