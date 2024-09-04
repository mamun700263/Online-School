from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SkillSerializer, CourseSerializer
from .models import SkillModel, CourseModel
from accounts.views import send_email

class SkillView(viewsets.ModelViewSet):
    authentication_classes = [] 
    permission_classes = [AllowAny] 
    queryset = SkillModel.objects.all()
    serializer_class = SkillSerializer
class CourseView(APIView):
    serializer_class = CourseSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            recipient_list = [course.taken_by.user.email]  # Assuming single teacher; update if multiple teachers
            context = {'course': course}
            send_email(
                subject="Course Upload Successful",
                template_name="email/upload_email.html",
                context=context,
                recipient_list=recipient_list
            )
            return Response({'message': 'Course created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny] 
    serializer_class = None
    model = None

    def get(self, request):
        items = self.model.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)



class SkillListView(ListView):
    authentication_classes = [] 
    permission_classes = [AllowAny] 
    serializer_class = SkillSerializer  
    model = SkillModel

class CourseListView(ListView):
    authentication_classes = [] 
    permission_classes = [AllowAny] 
    serializer_class = CourseSerializer
    model = CourseModel
