from django.db import models
from accounts.models import TeacherAccount

class SkillModel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class CourseModel(models.Model):
    name = models.CharField(max_length=120)
    taken_by = models.ManyToManyField(TeacherAccount)
    thumbnail = models.ImageField(upload_to='skill/thumbnails')
    paid = models.BooleanField()
    price = models.IntegerField(null=True, blank=True)
    approximate_time_to_finish = models.IntegerField(help_text="Time in hours")
    rating = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        teachers = ", ".join([f"{teacher.user.first_name} {teacher.user.last_name}" for teacher in self.taken_by.all()])
        return f"{self.name} taken by {teachers}"
