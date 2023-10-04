from django import forms
from django.forms import ClearableFileInput, ModelForm,TextInput,Textarea,FileInput,Select,ImageField
from .models import Course,Comment,FileField
from ckeditor.widgets import CKEditorWidget

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if data is None:
            return []
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    

class UploadCourseForm(ModelForm):
    # source_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,'required':False}))
    # source_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    # source_file  = forms.ClearableFileInput(attrs={"allow_multiple_selected": True,'required':False})



 
    class Meta:
        model = Course
        fields = ('course_name','card_desc','image','content','video_url',)
        
        widgets = {
            'course_name': TextInput(attrs={'label':'Course Name *','class': 'form-control', 'placeholder': 'Enter course name'}),
            'card_desc': TextInput(attrs={'label':'Course Description *','class': 'form-control', 'placeholder': 'Enter card description'}),
            'video_url': TextInput(attrs={'label':'Video Url ','class': 'form-control', 'placeholder': 'Enter video URL','required':False}),
            'content': CKEditorWidget(),  # Use the CKEditor widget for the 'content' field

        
            # 'source_file':ClearableFileInput(attrs={'allow_multiple_selected': True,'required':False}),
    #         # 'source_file': FileInput(attrs={'class': 'form-control', 'required': False}),
            # 'source_file': forms.FileInput(attrs={'multiple': True}),

    #   
        }
        image = forms.ImageField(
        label='Card Image*',  # Add a label with an asterisk (*) to indicate required
        required=True,  # Set the field as required
    )
    # def clean_source_file(self):
    #     source_files = self.cleaned_data.get('source_file', [])  # Initialize as an empty list
    #     max_file_size = 1048576000  # 1GB in bytes
    #     files_too_large = []
    #     valid_source_files = []

    #     for source_file in source_files:
    #         if source_file.size > max_file_size:
    #             files_too_large.append(source_file)
    #         else:
    #             valid_source_files.append(source_file)

    #     if files_too_large:
    #         too_large_files = ", ".join([file.name for file in files_too_large])
    #         raise forms.ValidationError(
    #             f"File(s) too large. Maximum file size is 1GB. The following file(s) are too large: {too_large_files}",
    #             code='invalid_file_size'
    #         )

    #     return valid_source_files




#     course_name = forms.CharField(max_length=256,widget=forms.TextInput(
#         attrs={'class':'form-control','placeholder':'Enter course name'}
#     )),
#     card_desc = forms.CharField(
#         max_length=256,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter card description'})
#     ),
# card_image = forms.ImageField()


class FileUploadForm(ModelForm):

    class Meta:
        model = FileField
        fields = ('source_file',)

    source_file = MultipleFileField(required=False)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {            
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Write comment...'}),


        }