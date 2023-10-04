from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from ols_app.models import Course,Enroll,Comment,FileField
from django.contrib.auth import get_user_model
import uuid
import os
from ols_app.forms import UploadCourseForm,CommentForm,FileUploadForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic.edit import FormView
from ols_app.decorators import teacher_required
from django.http import JsonResponse
User = get_user_model()
# Create your views here.
def index_page(request):
    return render(request,'index.html')

def course_page(request):

    courses = Course.objects.order_by('-id')[:12]
    context ={'courses':courses}
    return render(request,"course.html",context)

def about_page(request):
    return render(request,"about.html")

def contact_page(request):
    return render(request,"contact.html")

def teacher_page(request):
    teachers = User.objects.filter(role='teacher').order_by('-id')[:12]
    print(teachers)
    context = {'teachers':teachers}
    return render(request,"teacher.html",context)

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
            enrolled = Enroll.objects.filter(owner=request.user,course = Course.objects.get(id=course_id)).exists()
            response_data={}
            print(f"Enrolled answer: '  {enrolled}")

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
    comments = Comment.objects.filter(course=course).all().order_by('-id')[:5]
    files = FileField.objects.filter(course=course).all().order_by('-id')
    print(files)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.course = course
            comment.user = request.user
            comment.save()
    else:
        form = CommentForm()
    context={'course':course,'form':form,"comments":comments,"files":files}
    return render(request,'detail_page.html',context) 


@login_required(login_url='user:teacher_login')
@teacher_required
def teacher_dashboard_page(request):
    user = request.user
    print(f'User Role: {user.role}')
    print('Teacher Dashboard View Accessed')  # Add a debug print
    created_course = Course.objects.filter(uploaded_by = request.user).all().order_by('-id')
    context = {'created_course':created_course}
    return render(request,'teacher_dashboard.html',context)

def is_teacher(user):
    return user.is_authenticated and user.role == "teacher"



@login_required(login_url='user:teacher_login')
# @user_passes_test(is_teacher,login_url="user:teacher_login")
@teacher_required
def teacher_upload_view(request):
    fileField = FileUploadForm()  # Initialize the form
    print("Started here")

    if request.method == "POST":
        form = UploadCourseForm(request.POST,request.FILES)
        # fileField = FileUploadForm(request.FILES or None)

        files = request.FILES.getlist('source_file')    
        if form.is_valid():
            course = form.save(commit=False)
            course.uploaded_by = request.user
            print("I am first debug")
            course.save()
            
            max_file_size = 1048576000  # 1GB in bytes
            files_too_large = []
            if len(files) > 0:
                for f in files:
                    if f.size > max_file_size:
                        files_too_large.append(f.name)

                if files_too_large:
                    too_large_files = ", ".join(files_too_large)
                    for file_name in files_too_large:
                        form.add_error(
                            'source_file',
                            ValidationError(
                                f"File '{file_name}' is too large. Maximum file size is 1GB.",
                                code='invalid_file_size'
                            )
                        )
            for i in files:
                FileField.objects.create(course=course,source_file=i)
        
            # course.uploaded_by = request.user
   
            messages.add_message(request, messages.INFO, "Uploaded Successfully")
            return redirect('ols_name:course_upload')
        else:
            for field, errors in form.errors.items():
                    for error in errors:
                        messages.add_message(request, messages.ERROR, f"Error in {field}: {error}")
    else:
        form = UploadCourseForm()        
        
    context={'form':form,'fileField':fileField}
    return render(request,'upload_course.html',context)

@login_required
def add_comment_to_course(request,courseid):
    course = Course.objects.get(pk=courseid)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.course = course
            comment.user = request.user
            comment.save()
    else:
        form = CommentForm()
    return render(request,'ols_name:detail',{'form':form})


# @login_required(login_url='user:teacher_login')
# class teacher_upload_view(FormView):
#     form_class = UploadCourseForm
#     template_name = 'upload_course.html'  # Replace with your template.
#     success_url = "upload_course.html"  # Replace with your URL or reverse().

#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             for f in files:
#                 ...  # Do something with each file.
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
