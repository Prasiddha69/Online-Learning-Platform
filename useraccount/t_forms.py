from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class TeacherRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter your username"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter your password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Confirm your password"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter your email address"}))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={"class": "form-control","required":"required"}))

    class Meta:
        model = User
        fields = ('username','email','password1','password2','role')




class TeacherLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


# class TeacherLoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))