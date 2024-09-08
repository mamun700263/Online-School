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
    
    
    
    
from rest_framework.permissions import IsAuthenticated

class CourseView(APIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in to upload a course

    def post(self, request):
        # Print statements for debugging
        print("Request Data:", request.data)
        print("User:", request.user)
        
        # Attach the logged-in user as the teacher (taken_by) to the course data
        data = request.data.copy()  # Make a mutable copy of request data
        data['taken_by'] = request.user.id  # Assign the logged-in user's ID to 'taken_by'
        
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            # Save the course, with the 'taken_by' field set to the logged-in user
            course = serializer.save()


            recipient_list = [request.user.email] 
            print(recipient_list)
            context = {'course': course}
            send_email(
                subject="Course Upload Successful",
                template_name="email/upload_email.html",
                context=context,
                recipient_list=recipient_list
            )

            return Response({'message': 'Course created successfully!'}, status=status.HTTP_201_CREATED)
        
        # Return errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(taken_by=self.request.user)

    def get(self, request):
        courses = CourseModel.objects.all()  # Fetch all courses
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data)


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
