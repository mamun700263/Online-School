from django.db import models
from django.db.models import Avg
from accounts.models import TeacherAccount,StudentAccount

class SkillModel(models.Model):
    """
    this is just a skill and teachers can apply
    """
    name = models.CharField(max_length=50, unique=True)
    thumbnail = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name
    

    
class CourseModel(models.Model):
    name = models.CharField(max_length=80)
    taken_by = models.ForeignKey(TeacherAccount, on_delete=models.CASCADE, related_name='account',default=1)
    students = models.ManyToManyField(StudentAccount, related_name='enrolled_courses', blank=True)
    description = models.TextField(default="description")  
    skills = models.ManyToManyField(SkillModel)  
    thumbnail = models.URLField(null=True, blank=True)
    paid = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    time = models.IntegerField(help_text="Time in hours")
    rating = models.FloatField(default=0, null=True, blank=True)


    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        reviews = self.reviews.all() 
        if reviews.exists():
            total_rating = sum(int(review.rating)  for review in reviews) 
            self.rating = total_rating
            average=total_rating / reviews.count()  
            return round(average, 2)
        return 0 


class Enrollment(models.Model):
    user = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')