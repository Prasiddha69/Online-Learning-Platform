from django.urls import path,include
from useraccount.views import login_view,register_view
app_name="user"
urlpatterns = [
    path('login/',login_view,name="login"),
    path('register/',register_view,name="register")
]
