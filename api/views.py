from django.http import HttpResponse
from rest_framework import generics

from .models import User
from .serializers import UserSerializer


def index(request):
    return HttpResponse("Hello, Server!")

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer