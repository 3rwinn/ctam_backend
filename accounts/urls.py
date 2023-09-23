from django.urls import path, include

from . import views
from .api import LoginAPI, UserAPI, RegisterAPI, UserList, UserDelete, UserMissionList, UserMissionDetail, ChangePasswordView
urlpatterns = [
    ### API
    # path('api/auth', include('knox.urls')),
    path('auth/login', LoginAPI.as_view()),
    path('auth/user', UserAPI.as_view()),
    path('auth/register', RegisterAPI.as_view()),
    path("auth/users", UserList.as_view()),
    path("auth/users/<int:pk>", UserDelete.as_view()),
    path("auth/users/missions", UserMissionList.as_view()),
    path("auth/users/missions/<int:mission_id>", UserMissionDetail.as_view()),
    path("auth/change-password", ChangePasswordView.as_view()),

]
