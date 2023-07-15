from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from useraccount.forms import RegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
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

        try:
                valid_user = authenticate(request,email=user_email, password=user_pass)
                print(valid_user)
                if valid_user is None or isinstance(valid_user, AnonymousUser):
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
        print("Form doesnot")
        form = RegisterForm()

    
    context = {
        "form":form,
    }
    return render(request,"register.html",context)

