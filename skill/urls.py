from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillView, CourseView, SkillsListView, CourseListView


router = DefaultRouter()
router.register(r'skills', SkillView, basename='skill')

urlpatterns = [
    # router URLs
    path('', include(router.urls)),

    # API views for Courses
    path('courses/', CourseView.as_view(), name='create-course'),
    path('courses/list/', CourseListView.as_view(), name='list-courses'),

    # API views for Skills
    path('skills/list/', SkillsListView.as_view(), name='list-skills'),
]
