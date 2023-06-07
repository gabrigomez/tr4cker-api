from django.urls import path
from . import views
from .views import RegisterUserView, UsersListView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.index),
    path('register', RegisterUserView.as_view()),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users', UsersListView.as_view()),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),    
]
