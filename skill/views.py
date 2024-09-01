
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import viewsets
from .serializers import SkillSerializer, CourseSerializer
from .models import SkillModel, CourseModel
from accounts.views import send_email
# Create your views here.

class SkillView(viewsets.ModelViewSet):
    queryset = SkillModel.objects.all()  
    serializer_class = SkillSerializer

class CourseView(APIView):
    serializer_class = CourseSerializer
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            # Get the email addresses of the teachers associated with the course
            recipient_list = [teacher.user.email for teacher in course.taken_by.all()]
            # send the course as cotxt and make them in the html
            context = {'course': course}
            send_email(
                subject="Course Upload Successful",
                template_name="email/upload_email.html",
                context=context,
                recipient_list=recipient_list
            )
            return Response({'message': 'Course created successfully!'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
