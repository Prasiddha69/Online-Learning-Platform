from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index_page(request):
    return render(request,'index.html')

def course_page(request):
    return render(request,"course.html")

def about_page(request):
    return render(request,"about.html")

def contact_page(request):
    return render(request,"contact.html")

def teacher_page(request):
    return render(request,"teacher.html")

@login_required
def dashboard_page(request):
    return render(request,'dashboard.html')