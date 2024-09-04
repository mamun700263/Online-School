from django.urls import path
# from .views import uv
from .views import StudentAccountCreateView, TeacherAccountCreateView,activate,UserLoginApiView,UserLogout,StudentListView,TeacherListView,ProfileView

urlpatterns = [
    path('student/', StudentAccountCreateView.as_view(), name='student'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('teacher/', TeacherAccountCreateView.as_view(), name='teacher'),
    path('student_list/', StudentListView.as_view(), name='s_list'),
    path('teacher_list/', TeacherListView.as_view(), name='t_list'),
    path('activate/<uid64>/<token>/',activate),
    path('login/',UserLoginApiView.as_view(),name='login'),
    path('logout/',UserLogout.as_view(),name='logout'),
]


