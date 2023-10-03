from django.contrib import admin
from ols_app.models import Course,Enroll,Comment,FileField
# Register your models here.
admin.site.register(Course)
admin.site.register(Enroll)
admin.site.register(Comment)

# admin.register(FileFieldAdmin)
class FileFieldAdmin(admin.ModelAdmin):
    list_display=('id','source_file','course')

admin.site.register(FileField,FileFieldAdmin)
