from django.urls import path
from . import views
from .views import RegisterUserView

urlpatterns = [
    path('', views.index),
    path('register', RegisterUserView.as_view())    
]
