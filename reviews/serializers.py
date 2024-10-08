from rest_framework import serializers
from .models import ReviewModel

class ReviewSerializer(serializers.ModelSerializer):
    given_by_name = serializers.SerializerMethodField()
    given_by_img = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    class Meta:
        model = ReviewModel
        fields = ['id','rating','text','course','given_by','given_by_name','given_by_img','course_name']
        read_only_fields = ['id','given_by_name','given_by_img','course_name']

    def get_given_by_name(self, obj):
        return f"{obj.given_by.user.first_name}  {obj.given_by.user.last_name}"  
    
    def get_course_name(self, obj):
        return f"{obj.course.name}"
    
    def get_given_by_img(self,obj):
        return f"{obj.given_by.profile_picture}"
        # Override the rating field to reflect the average rating

