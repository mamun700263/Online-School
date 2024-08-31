from django.db import models
from accounts.models import StudentAccount
from skill.models import CourseModel

STARS = (
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
)

class ReviewModel(models.Model):
    given_by = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, related_name='reviews')
    rating = models.CharField(choices=STARS, max_length=5)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.given_by.user.first_name} {self.given_by.user.last_name} - {self.rating}"
