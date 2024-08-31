from django.contrib import admin
from .models import StudentAccount,TeacherAccount
# Register your models here.f
admin.site.register(StudentAccount)
admin.site.register(TeacherAccount)