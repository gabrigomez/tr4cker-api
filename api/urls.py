from django.urls import path
from . import views
from .views import RegisterUserView, UsersListView, UserOptionsView, LoginUserView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.index),
    path('register', RegisterUserView.as_view()),
    # path('login', LoginUserView.as_view()),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/<int:id>', UserOptionsView.as_view()),
    path('users', UsersListView.as_view()),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),    
]
