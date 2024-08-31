from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SkillSerializer,CourseSerializer
from .models import SkillModel,CourseModel

# Create your views here.
class SkillView(viewsets.ModelViewSet):
    queryset = SkillModel.objects.all()  
    serializer_class = SkillSerializer


class CourseView(viewsets.ModelViewSet):
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer