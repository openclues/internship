from django.contrib import admin

# Register your models here.
from django.contrib.admin import site

from .models import Student, UserAccount , Practise , PractiseSubmission , Coordinator , CareerCenter
admin.site.register(Student)
admin.site.register(Practise)
admin.site.register(UserAccount)
admin.site.register(PractiseSubmission)
admin.site.register(Coordinator)
admin.site.register(CareerCenter)
