from typing import Any
from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth import get_user_model
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
import re,os
from OLS.settings import MEDIA_ROOT

from PIL import Image

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
    image = models.ImageField(upload_to="images/",blank=False,unique=True)
    content = RichTextUploadingField(blank=True,null=True)

    video_url = EmbedVideoField(blank=True,null=True)  # same like models.URLField()
    video_file = models.FileField(upload_to='uploads/videos/', null=True, verbose_name="video",blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,default="admin")  # Assuming you have a User model

    def __str__(self):
        return f"{self.course_name}"
    


    def save(self, *args, **kwargs):
        super(Course,self).save(*args, **kwargs)

        if self.content:
            #Compress CKEditor image
            self.compress_ckeditor_images()

        if self.image:
            #Compress normal image
            self.compress_normal_image()            


    def compress_ckeditor_images(self):

        # Finding the image from ckeditor
        if self.content:
            # Regular expression to match CKEditor image tags
            pattern = r'<img[^>]+src="([^">]+)"[^>]*>'

            image_tags = re.findall(pattern,self.content)

            for image_url in image_tags:
                if image_url.lower().endswith('.jpg') or image_url.lower().endswith('.jpeg'):
                    image_path = self.get_image_path(image_url)
                    if image_path:
                        self.compress_image(image_path)


    def compress_normal_image(self):
        #Compress the normal image
        if self.image:
            image_path = self.image.path
            self.compress_image(image_path)

    def get_image_path(self,image_url):
         #Remove the protocol and domain from the image URL
        # to get the relative path
        relative_path = image_url.replace(settings.MEDIA_URL, "")

        # Join the relative path with the base media root to get the full file path
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        return full_path
    
    def compress_image(self,image_path):
        image = Image.open(image_path)
        image.save(image_path,quality=60,optimize=True)

class FileField(TimeStampModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    source_file = models.FileField(upload_to='uploads/file/',null=True,blank=True)  # Specify allowed file extensions

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



class ContactCustomer(TimeStampModel):
    username = models.CharField(max_length=250)
    number = models.CharField(max_length=256)
    useremail = models.CharField(max_length=256)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"Contacted by {self.username}"