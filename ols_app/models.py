from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth import get_user_model
from django.conf import settings
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
    card_image = models.ImageField(upload_to='uploads/images/')
    video_url = EmbedVideoField(blank=True,null=True)  # same like models.URLField()
    video_file = models.FileField(upload_to='uploads/videos/', null=True, verbose_name="video",blank=True)
    paragraph = models.TextField(blank=True, null=True)
    source_file = models.FileField(upload_to='uploads/file/',null=True,blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)  # Assuming you have a User model

    def __str__(self):
        return f"{self.course_name}"




class Enroll(TimeStampModel):
    has_finished = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_enrolled = models.BooleanField(default=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner} --> {self.course}"
    






