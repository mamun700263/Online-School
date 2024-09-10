from rest_framework import serializers
from .models import SkillModel,CourseModel
from accounts.models import TeacherAccount
from accounts.serializers import TeacherAccountSerializer

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillModel
        fields = "__all__"



class CourseSerializer(serializers.ModelSerializer):
    print('form the serializer')
    taken_by_name = serializers.SerializerMethodField()
    taken_by_img = serializers.SerializerMethodField()
    skills_list = serializers.SerializerMethodField()

    class Meta:
        model = CourseModel
        fields = ['id','name','taken_by','description','skills','thumbnail','paid','price','time','rating','taken_by_name','taken_by_img','skills_list']
        read_only_fields = ['rating','taken_by_name','taken_by_img','skills_list']  # teacher can't add rating


    def get_taken_by_name(self, obj):
        return f"{obj.taken_by.user.username} "  # Return full name of the teacher
    

    def get_taken_by_img(self,obj):
        return f"{obj.taken_by.profile_picture}"
    
    def get_skills_list(self, obj):
        return [{'name': skill.name} for skill in obj.skills.all()]