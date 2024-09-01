
from rest_framework import serializers

from .models import SkillModel,CourseModel

from accounts.models import TeacherAccount

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillModel
        fields = "__all__"



class CourseSerializer(serializers.ModelSerializer):
    """
    This addition thing is required to avoid the primary key problem
    """
    taken_by = serializers.PrimaryKeyRelatedField(
        queryset=TeacherAccount.objects.all(),
        many=True, 
        required=False ,
    )

    class Meta:
        model = CourseModel
        fields = '__all__'