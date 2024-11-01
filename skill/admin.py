from django.contrib import admin
from .models import SkillModel, CourseModel,Enrollment

class CourseModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'paid', 'price', 'time', 'rating')
    # filter_horizontal = ('taken_by',) 

admin.site.register(SkillModel)
admin.site.register(Enrollment)
admin.site.register(CourseModel, CourseModelAdmin)
