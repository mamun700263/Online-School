from django.contrib.auth.models import User
from django.db import models
import uuid

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    date_of_birth = models.DateField(blank=True, null=True)
    unique_id = models.CharField(unique=True,  max_length=12,null=True,blank=True)
    bio = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)  

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Create a new User if it doesn't exist
        if not self.user_id:
            self.user = User.objects.create(
                username=self.username,
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
            )
            self.user.set_password(self.password)
            self.user.save()
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        raise NotImplementedError("Subclasses should implement this method.")


class StudentAccount(Account):
    def generate_unique_id(self):
        return f"ST-{uuid.uuid4().hex[:8].upper()}"

class TeacherAccount(Account):
    def generate_unique_id(self):
        return f"TE-{uuid.uuid4().hex[:8].upper()}"
