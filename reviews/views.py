from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from accounts.models import StudentAccount
from skill.models import CourseModel,Enrollment
from .serializers import ReviewSerializer
from .models import ReviewModel
from django.shortcuts import get_object_or_404






from rest_framework.exceptions import ValidationError

class ReviewView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        try:
            reviews = ReviewModel.objects.all()
            review_serializer = ReviewSerializer(reviews, many=True)
            return Response(review_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Unable to fetch reviews at the moment.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request):
        print(request.data)
        try:
            # Get the student account for the logged-in user
            account = get_object_or_404(StudentAccount, user=self.request.user)
            # taccount = get_object_or_404(StudentAccount, user=self.request.user)

            # if taccount:
            #     return Response({'error': 'Only students can give reviews.'}, status=status.HTTP_403_FORBIDDEN)

            # Ensure the user is a student
            if not account:
                return Response({'error': 'Only students can give reviews.'}, status=status.HTTP_403_FORBIDDEN)

            course_id = request.data.get('course')
            if not course_id:
                return Response({'error': 'Course ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the course based on the course_id
            course = get_object_or_404(CourseModel, id=course_id)

            # Check if the student is enrolled in the course
            enrolled = Enrollment.objects.filter(user=account, course=course).exists()
            print(f"Enrollment check: user={account}, course={course}, enrolled={enrolled}")  # Debugging output

            if not enrolled:
                return Response({'error': 'Only enrolled students can give reviews.'}, status=status.HTTP_403_FORBIDDEN)

            # Check if the student has already given a review for this course
            existing_review = ReviewModel.objects.filter(given_by=account, course=course).first()
            if existing_review:
                return Response({'error': 'You have already submitted a review for this course.'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate the submitted review data
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(given_by=account, course=course)
                return Response({'message': 'Review given successfully!'}, status=status.HTTP_201_CREATED)

            # Return error if validation fails
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ve:
            return Response({'error': 'Validation error', 'details': ve.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Error: {e}")  # Add better exception logging
            return Response({'error': 'Teachers cant review'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ReviewDeatil(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    queryset = ReviewModel.objects.all()  


    def get(self, request,pk):
        """at first gett all objects and then filter form them"""
        try:
            reviews = ReviewModel.objects.get(id=pk)
        except ReviewModel.DoesNotExist:
            return Response({'error':"review not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(reviews)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, *args, **kwargs):
        review_id = kwargs.get('pk')
        
        try:
            review = ReviewModel.objects.get(id=review_id)
            print('try patch reviewdetail veiw found',review)
        except ReviewModel.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(review, data=request.data, partial=True)
        print('given_by' , review.given_by.user)
        print('requested by' , request.user.account.user)
        
        if review.given_by.user != request.user.account.user:
            return Response({'error': 'You do not have permission to update this REview'}, status=status.HTTP_403_FORBIDDEN)


        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Course updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        review_id = kwargs.get('pk')
        try:
            review = ReviewModel.objects.get(id=review_id)
            review.delete()
            return Response({'message': 'review deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except ReviewModel.DoesNotExist:
            return Response({'error': 'review not found'}, status=status.HTTP_404_NOT_FOUND)


