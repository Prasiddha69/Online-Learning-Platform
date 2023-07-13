from django.shortcuts import render,redirect
from useraccount.forms import RegisterForm
# Create your views here.
def login_view(request):
    return render(request,"login.html")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("form saved")
            return redirect('user:register')
    else:
        print("Form doesnot")
        form = RegisterForm()

    

    return render(request,"register.html",{"form":form})

