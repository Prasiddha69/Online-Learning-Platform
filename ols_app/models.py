from typing import Any
from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import FileExtensionValidator
User = get_user_model()
# Create your models here.
class TimeStampModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True



class Course(TimeStampModel):
    course_name = models.CharField(max_length=256)
    card_desc = models.CharField(max_length=256)
    video_url = EmbedVideoField(blank=True,null=True)  # same like models.URLField()
    video_file = models.FileField(upload_to='uploads/videos/', null=True, verbose_name="video",blank=True)
    paragraph = models.TextField(blank=False,null=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,default="admin")  # Assuming you have a User model

    def __str__(self):
        return f"{self.course_name}"



class FileField(TimeStampModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    source_file = models.FileField(upload_to='uploads/file/',null=True,blank=True,validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx','txt'])  # Specify allowed file extensions
    ])

    def __str__(self):
        return f"{self.course} ---> {self.source_file}"






class Enroll(TimeStampModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_enrolled = models.BooleanField(default=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner} --> {self.course}"
    




class Comment(TimeStampModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str__(self):
        return f"Comment by {self.user.username}"

