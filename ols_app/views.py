from django.shortcuts import render

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

