from rest_framework import serializers
from .models import SkillModel,CourseModel

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillModel
        fields = "__all__"



class CourseSerializer(serializers.ModelSerializer):
    taken_by_name = serializers.SerializerMethodField()
    taken_by_img = serializers.SerializerMethodField()
    skills_list = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = CourseModel
        fields = ['id','name','taken_by','description','skills','thumbnail','paid','price','time','rating','taken_by_name','taken_by_img','skills_list','average_rating']
        read_only_fields = ['rating','taken_by_name','taken_by_img','skills_list','average_rating']  


    def get_taken_by_name(self, obj):
        return f"{obj.taken_by.user.username} "  
    
    def get_average_rating(self, obj):
        return obj.get_average_rating()
    
    def get_taken_by_img(self,obj):
        return f"{obj.taken_by.profile_picture}"
        # Override the rating field to reflect the average rating
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = representation.pop('average_rating')  
        return representation
    
    def get_skills_list(self, obj):
        return [{'name': skill.name} for skill in obj.skills.all()]