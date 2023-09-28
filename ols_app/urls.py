from django.urls import path
from ols_app.views import index_page,course_page,contact_page,about_page,teacher_page,dashboard_page,add_to_dashboard,detail_page,teacher_dashboard_page,teacher_upload_view
app_name="ols_name"
urlpatterns = [
    path('', index_page,name="home"),
    path('about/', about_page,name="about"),
    path('contact/', contact_page,name="contact"),
    path('course/', course_page,name="course"),
    path('teacher/', teacher_page,name="teacher"),
    path('dashboard/', dashboard_page,name="dashboard"),
    path('add-to-dashboard/', add_to_dashboard,name="Enrolled"),
    path('detail-page/<int:courseid>/', detail_page,name="detail"),
    path('teacher-dashboard/', teacher_dashboard_page,name="teacher_dashboard"),
    path('upload-course/', teacher_upload_view,name="course_upload"),











]
