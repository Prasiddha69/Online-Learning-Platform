from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from useraccount.forms import RegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .t_forms import TeacherRegistrationForm,TeacherLoginForm
from .models import User
from django.contrib.auth.views import LoginView

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        # User = get_user_model()
        try:
            user = User.objects.get(email=email,role='student')
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None




# Create your views here.
def login_view(request):
    if request.method == "POST":
        user_email = request.POST.get('user_email_log')
        user_pass = request.POST.get('user_pass_log')
        email_test = request.POST['user_email_log']
        print(email_test)

        print(user_email)
        print(user_pass)
        if ((user_email == '' or None) or (user_pass == '' or None)):
            messages.add_message(request, messages.ERROR, "Please complete the form")
            return redirect("user:login")
                          
        try:
                valid_user = authenticate(request,email=user_email, password=user_pass)
                print(valid_user)
                if valid_user is None or isinstance(valid_user, AnonymousUser) and valid_user.role == 'teacher':
                    messages.add_message(request, messages.ERROR, "Invalid email or password")
                    return redirect("user:login")
                login(request, valid_user)
                return redirect("ols_name:home")

        except Exception as e:
                messages.add_message(request, messages.ERROR, f"An error occurred: {str(e)}")
                return redirect("user:login")

    return render(request,"login.html")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("form saved")
            messages.add_message(request, messages.INFO, "Registered Successfully")
    else:
        
        form = RegisterForm()

    
    context = {
        "form":form,
    }
    return render(request,"register.html",context)

@login_required
def logout_view(request):
    logout(request)
      # Set the session to expire immediately
    request.session.set_expiry(0)
    return redirect('ols_name:home')



def teacher_register_view(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'teacher'
            user.save()
            user.backend = 'useraccount.backends.TeacherBackend'
            messages.add_message(request, messages.INFO, "Registered Successfully")


    else:
        form=TeacherRegistrationForm()
    return render(request,'teacher_register.html',{'form':form})




def teacher_login_view(request):
    form = TeacherLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)

            if user is not None and user.role == 'teacher':
                # Explicitly specify the authentication backend
                # user.backend = 'useraccount.views.UsernameBasedAuthenticationBackend'
                login(request, user)
                # Add your login success logic here
                return redirect('ols_name:teacher_dashboard')
            else:
                    messages.add_message(request, messages.ERROR, "Please enter valid credentials")


    return render(request, 'teacher_login.html', {'form': form})

