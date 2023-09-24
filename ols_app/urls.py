from django.urls import path
from ols_app.views import index_page,course_page,contact_page,about_page,teacher_page,dashboard_page
app_name="ols_name"
urlpatterns = [
    path('', index_page,name="home"),
    path('about/', about_page,name="about"),
    path('contact/', contact_page,name="contact"),
    path('course/', course_page,name="course"),
    path('teacher/', teacher_page,name="teacher"),
    path('dashboard/', dashboard_page,name="dashboard"),







]
