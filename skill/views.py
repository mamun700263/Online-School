from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SkillSerializer, CourseSerializer
from .models import SkillModel, CourseModel
from accounts.models import TeacherAccount
from accounts.views import send_email





#i will be able to see all skills
class SkillView(viewsets.ModelViewSet):
    authentication_classes = [] 
    permission_classes = [AllowAny] 
    queryset = SkillModel.objects.all()
    serializer_class = SkillSerializer
    
    
    
    


class CourseView(APIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Request Data:", request.data)
        print("User:", request.user)
        print("User id:", request.user.account.id)

        data = request.data.copy()
        data['taken_by'] = request.user.account.id

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            print(serializer.validated_data)
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        try:
            account = TeacherAccount.objects.get(user=user)  # Assuming the teacher account is linked to the user
        except TeacherAccount.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get all courses uploaded by this teacher
        courses = CourseModel.objects.filter(taken_by=account)

        # Serialize the course data
        serializer = self.serializer_class(courses, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListView(APIView):
    authentication_classes = []  # Allow any user (even unauthenticated users)
    permission_classes = [AllowAny]  # No special permissions required
    serializer_class = None  # Will be defined in the subclass
    model = None  # Will be defined in the subclass

    def get(self, request):
        # Fetch all objects from the model
        items = self.model.objects.all()
        
        # Serialize the data using the serializer class
        serializer = self.serializer_class(items, many=True)
        
        # Return the serialized data in the response
        return Response(serializer.data)  # Use `.data` to return serialized data


# Skill List View
class SkillListView(ListView):
    serializer_class = SkillSerializer  # Serializer for the Skill model
    model = SkillModel  # Skill model to fetch data from




class CourseListView(generics.ListAPIView):
    
    authentication_classes = []  # Allow any user (even unauthenticated users)
    permission_classes = [AllowAny]  # No special permissions required
    serializer_class = CourseSerializer

    # Override get_queryset to add filtering logic
    def get_queryset(self):
        queryset = CourseModel.objects.all()
        print(queryset)
        skill_id = self.request.query_params.get('skill_id', None)
        if skill_id:
            # Filter courses by the skill's ID
            queryset = queryset.filter(skills__id=skill_id)
        return queryset
    








    
    def patch(self, request):
        user = request.user
        try:
            account = CourseModel.objects.get(user=user)
        except CourseModel.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        print(data)
        # user.username = data.get('username', user.username)
        # user.first_name = data.get('first_name', user.first_name)
        # user.last_name = data.get('last_name', user.last_name)
        # user.email = data.get('email', user.email)
        # user.save()

        # account.mobile = data.get('mobile', account.mobile)
        # account.date_of_birth = data.get('date_of_birth', account.date_of_birth)
        # account.profile_picture = data.get('profile_picture', account.profile_picture)  
        # account.save()
        # return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)




class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]  
    serializer_class = CourseSerializer
    queryset = CourseModel.objects.all()  

    def get(self, request, pk):
        print('hello',pk)
        try:
            course = CourseModel.objects.get(id=pk)
        except CourseModel.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
