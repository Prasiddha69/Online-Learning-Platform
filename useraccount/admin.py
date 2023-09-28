from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from useraccount.models import User
# admin.site.register(User,UserAdmin)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')


    
admin.site.register(User,CustomUserAdmin)
