from django.forms import ModelForm,TextInput,Textarea,FileInput,Select,forms
from .models import Course,Comment

class UploadCourseForm(ModelForm):
 
    class Meta:
        model = Course
        fields = ('course_name','card_desc','card_image','video_url','paragraph','source_file')
        
        widgets = {
            'course_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course name'}),
            'card_desc': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter card description'}),
            'video_url': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter video URL','required':False}),
            'source_file': FileInput(attrs={'class': 'form-control','required':False}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {            
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Write comment...'}),


        }