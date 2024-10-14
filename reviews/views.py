from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from accounts.models import StudentAccount
from skill.models import CourseModel
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
        try:
            account = get_object_or_404(StudentAccount, user=self.request.user)
            
            # Check if the account is valid (ensuring the user is a student)
            if account is None:
                return Response({'error': 'Only students can give reviews.'}, status=status.HTTP_403_FORBIDDEN)
            
            # Check if the user has already given a review
            existing_review = ReviewModel.objects.filter(given_by=account).first()
            if existing_review:
                return Response({'error': 'You have already submitted a review.'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate the submitted review data
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(given_by=account)
                return Response({'message': 'Review given successfully!'}, status=status.HTTP_201_CREATED)

            # If validation fails, return error details
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ve:
            return Response({'error': 'Validation error', 'details': ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': 'Something went wrong.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


