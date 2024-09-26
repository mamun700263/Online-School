from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import ReviewView,ReviewDeatil


urlpatterns = [
    path('reviews/', ReviewView.as_view(), name='review-list'),  # Adjust as needed
    path('review_detail/<int:pk>/', ReviewDeatil.as_view(), name='review-detail'),  # Adjust as needed
]
