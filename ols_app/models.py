from django.db import models
from embed_video.fields import EmbedVideoField


# Create your models here.
class TimeStampModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True


class Course(TimeStampModel):
    course_name = models.CharField(max_length=256)
    desc = models.CharField(max_length=256)
    video_url = EmbedVideoField(blank=True,null=True)  # same like models.URLField()
    video_file = models.FileField(upload_to='videos/', null=True, verbose_name="video")
    
