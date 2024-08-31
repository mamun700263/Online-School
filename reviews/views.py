from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ReviewSerializer
from .models import ReviewModel

# Create your views here.
class ReviewView(viewsets.ModelViewSet):
    queryset = ReviewModel.objects.all()  
    serializer_class = ReviewSerializer
