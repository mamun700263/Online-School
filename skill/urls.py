from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillView, CourseView, SkillListView, CourseListView,CourseDetailView


router = DefaultRouter()
router.register(r'skills', SkillView, basename='skill')

urlpatterns = [
    # router URLs
    path('', include(router.urls)),

    # API views for Courses
    path('courses/', CourseView.as_view(), name='create-course'),
    path('courses/list/', CourseListView.as_view(), name='list-courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    # API views for Skills
    path('skills/list/', SkillListView.as_view(), name='list-skills'),
]
