
from rest_framework import serializers

from .models import SkillModel,CourseModel

from accounts.models import TeacherAccount

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillModel
        fields = "__all__"



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = ['name', 'description', 'skills', 'thumbnail', 'paid', 'price', 'time', 'rating', 'taken_by']
        read_only_fields = ['taken_by', 'rating']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            validated_data['taken_by'] = request.user.teacher_profile  
        return super().create(validated_data)
