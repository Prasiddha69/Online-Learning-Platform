from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from ols_app.models import Course,Enroll,Comment

from ols_app.forms import UploadCourseForm,CommentForm
from django.contrib.auth.models import User

from django.http import JsonResponse

# Create your views here.
def index_page(request):
    return render(request,'index.html')

def course_page(request):

    courses = Course.objects.all().order_by('-id')
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
    user = request.user
    print(f'User Role: {user.role}')
    print('Student Dashboard View Accessed')  # Add a debug print

    enrolled_course = Enroll.objects.filter(owner=request.user,is_enrolled = True).all().order_by('-id')
    print(enrolled_course)
    
    context = {'enrolled_course':enrolled_course}
    return render(request,'dashboard.html',context)

@login_required(login_url='user:login')
def add_to_dashboard(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == "POST":

            course_id = request.POST.get('course_id')
            print(course_id)
            enrolled = Enroll.objects.filter(owner=request.user,id=course_id,is_enrolled=True).exists()
            print(enrolled)

            if enrolled:
                response_data={'message':'Course is already in the dashboard'}


            if not enrolled:
                print('I am in') 
                obj = Course.objects.get(id=course_id)
                courseobj,created = Enroll.objects.get_or_create(
                    owner = request.user,
                    is_enrolled = True,
                    course=obj


                )
                if not created:
                    courseobj.save()
                    response_data={'message':'Course added to dashboard'}
                
            print(response_data)
            return JsonResponse(response_data)
    else:
        return JsonResponse({'message':'Invalid request'},status=400)



@login_required(login_url='user:login')
def detail_page(request,courseid):
    course = Course.objects.get(id=courseid)
    comments = Comment.objects.filter(course=course)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.course = course
            comment.user = request.user
            comment.save()
    else:
        form = CommentForm()
    context={'course':course,'form':form,"comments":comments}
    return render(request,'detail_page.html',context) 


@login_required(login_url='user:teacher_login')
def teacher_dashboard_page(request):
    user = request.user
    print(f'User Role: {user.role}')
    print('Teacher Dashboard View Accessed')  # Add a debug print
    created_course = Course.objects.filter(uploaded_by = request.user).all().order_by('-id')
    context = {'created_course':created_course}
    return render(request,'teacher_dashboard.html',context)


@login_required(login_url='user:teacher_login')
def teacher_upload_view(request):
    if request.method == "POST":
        form = UploadCourseForm(request.POST,request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.uploaded_by = request.user
            course.save()

        
            return redirect('ols_name:course_upload')
    else:
        form = UploadCourseForm()        

    return render(request,'upload_course.html',{'form':form})


# def add_comment_to_course(request,courseid):
#     course = Course.objects.get(pk=courseid)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.course = course
#             comment.user = request.user
#             comment.save()
#     else:
#         form = CommentForm()
#     return render(request,'ols_name:detail',{'form':form})