from rest_framework.routers import DefaultRouter
from .views import SkillView,CourseView
from django.urls import path,include
router = DefaultRouter()


router.register('skills',SkillView)
router.register('courses',CourseView)


urlpatterns = [
    path('',include(router.urls)),
]
