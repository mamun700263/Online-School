from rest_framework import serializers
from .models import SkillModel,CourseModel
from accounts.models import TeacherAccount
from accounts.serializers import TeacherAccountSerializer

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillModel
        fields = "__all__"



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = ['name','taken_by','description','skills','thumbnail','paid','price','time','rating']
        read_only_fields = ['rating','taken_by']  # teacher can't add rating

