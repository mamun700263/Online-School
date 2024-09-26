from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .serializers import SkillSerializer, CourseSerializer
from .models import SkillModel, CourseModel, Enrollment
from accounts.models import TeacherAccount, StudentAccount
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
            account = TeacherAccount.objects.get(user=user)  
        except TeacherAccount.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get all courses uploaded by this teacher
        courses = CourseModel.objects.filter(taken_by=account)

        # Serialize the course data
        serializer = self.serializer_class(courses, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    serializer_class = SkillSerializer
    model = SkillModel  




class CourseListView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'price']  # Optional: add more filterable fields
    authentication_classes = []  # Allow any user (even unauthenticated users)
    permission_classes = [AllowAny]  # No special permissions required
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = CourseModel.objects.all()
        skill_id = self.request.query_params.get('skill_id', None)
        if skill_id:
            queryset = queryset.filter(skills__id=skill_id)
        return queryset




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
    



class CourseUpdateView(APIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = CourseModel.objects.all()
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]  # Add this line

    def get(self, request, pk):
        try:
            course = CourseModel.objects.get(id=pk)
        except CourseModel.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        try:
            course = CourseModel.objects.get(id=course_id)
        except CourseModel.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        # print(course.taken_by.user.id, request.user.account.user.id)
        if course.taken_by.user.id != request.user.account.user.id:
            return Response({'error': 'You do not have permission to update this course'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(course, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Course updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        try:
            course = CourseModel.objects.get(id=course_id)
            course.delete()
            return Response({'message': 'Course deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except CourseModel.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request, course_id):
    account = StudentAccount.objects.get(user = request.user)
    user = request.user
    # Ensure the user has an associated StudentAccount
    try:
        student_account = StudentAccount.objects.get(user=user)

    except StudentAccount.DoesNotExist:
        return Response({'error': 'User account not found'}, status=status.HTTP_404_NOT_FOUND)
    
    course = get_object_or_404(CourseModel, id=course_id)
    
    # Check if the user is already enrolled in the course
    if course.students.filter(id=user.id).exists():
        return Response({'success': False, 'message': 'Already enrolled.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Add the user to the many-to-many relationship
    course.students.add(account)
    
    # Create a new enrollment record
    Enrollment.objects.create(user=student_account, course=course)
    
    return Response({'success': True}, status=status.HTTP_201_CREATED)
