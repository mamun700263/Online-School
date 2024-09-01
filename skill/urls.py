# from rest_framework.routers import DefaultRouter
# from .views import SkillView,CourseView
# from django.urls import path,include
# router = DefaultRouter()


# router.register('skills',SkillView)
# router.register('courses',CourseView)


# urlpatterns = [
#     path('',include(router.urls)),
# ]
from django.urls import path,include
from .views import SkillView, CourseView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('skills', SkillView)

urlpatterns = [
    path('courses/', CourseView.as_view(), name='course-create'),
    path('', include(router.urls)),
]