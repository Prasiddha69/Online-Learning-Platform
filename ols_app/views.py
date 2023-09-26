from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ols_app.models import Course,Enroll

from django.http import JsonResponse

# Create your views here.
def index_page(request):
    return render(request,'index.html')

def course_page(request):

    courses = Course.objects.all()


    context ={'courses':courses}
    return render(request,"course.html",context)

def about_page(request):
    return render(request,"about.html")

def contact_page(request):
    return render(request,"contact.html")

def teacher_page(request):
    return render(request,"teacher.html")

@login_required(login_url='user:login')
def dashboard_page(request):
    enrolled_course = Enroll.objects.all()
    context = {'enrolled_course':enrolled_course}
    return render(request,'dashboard.html',context)

@login_required(login_url='user:login')
def add_to_dashboard(request):
    if request.method == "POST" and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

        course_id = request.POST.get('course_id')
        is_enrolled = Enroll.objects.filter(owner=request.user,pk=course_id,has_finished=False).exists()
        if not is_enrolled: 
            obj,created = Enroll.objects.get_or_create(
                owner = request.user,
                is_enrolled = True,
                pk=course_id


            )
            obj.save()


            response_data = {'message':'Course added to dashboard'}
        else:

            response_data = {'message':'Course is already in the dashboard'}
        print(response_data)
        return JsonResponse(response_data)
    else:
        return JsonResponse({'message':'Invalid request'},status=400)

