from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillView, CourseView, SkillListView, CourseListView, CourseDetailView, CourseUpdateView,enroll_course


router = DefaultRouter()
router.register(r'skills', SkillView, basename='skill')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),

    # API views for Courses
    path('courses/', CourseView.as_view(), name='create-course'),
    path('courses/list/', CourseListView.as_view(), name='list-courses'),
    
    # Separate paths for detail and update
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),  # GET for retrieving a course
    path('course_update/<int:pk>/', CourseUpdateView.as_view(), name='course-update'),  # PATCH for updating a course

    # API views for Skills
    path('skills/list/', SkillListView.as_view(), name='list-skills'),


    #Api views for enrollment
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
]
