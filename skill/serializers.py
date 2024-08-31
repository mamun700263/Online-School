from rest_framework import serializers
from .models import SkillModel,CourseModel

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillModel
        fields = "__all__"



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = "__all__"


