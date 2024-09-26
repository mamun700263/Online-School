from rest_framework.views import APIView
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from accounts.models import StudentAccount
from skill.models import CourseModel
from .serializers import ReviewSerializer
from .models import ReviewModel




class ReviewView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny] 
    serializer_class = ReviewSerializer
    
    def get(self, request):
        reviews = ReviewModel.objects.all()
        review_serializer = ReviewSerializer(reviews, many=True)
        # print('the problem is here')
        return Response(review_serializer.data)

    def post(self, request):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Review given  successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


