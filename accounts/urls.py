from django.urls import path
# from .views import uv
from .views import StudentAccountCreateView, TeacherAccountCreateView,activate,UserLoginApiView,UserLogout

urlpatterns = [
    path('student/', StudentAccountCreateView.as_view(), name='student'),
    path('teacher/', TeacherAccountCreateView.as_view(), name='teacher'),
    path('activate/<uid64>/<token>/',activate),
    path('login/',UserLoginApiView.as_view(),name='login'),
    path('logout/',UserLogout.as_view(),name='logout'),
]


