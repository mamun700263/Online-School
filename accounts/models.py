from django.db import models
from django.contrib.auth.models import User
import uuid

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    date_of_birth = models.DateField()
    unique_id = models.CharField(unique=True, editable=False, max_length=12)
    bio = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='', blank=True, null=True)  

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()


        if isinstance(self, StudentAccount):
            self.profile_picture.field.upload_to = 'accounts/student_profiles/'
        elif isinstance(self, TeacherAccount):
            self.profile_picture.field.upload_to = 'accounts/teacher_profiles/'
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        raise NotImplementedError("Subclasses should implement this method.")




#this is for the students
class StudentAccount(Account):

    def generate_unique_id(self):
        return f"ST-{uuid.uuid4().hex[:8].upper()}"

#for the teachers
class TeacherAccount(Account):

    def generate_unique_id(self):
        return f"TE-{uuid.uuid4().hex[:8].upper()}"
