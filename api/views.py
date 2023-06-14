from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer, RegisterUserSerializer

def index(request):
    return HttpResponse("Hello, Server!")

class UsersListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get('email')
            password = make_password(serializer.data.get('password'))
            username = serializer.data.get('username')
            
            user = User(email=email, password=password, username=username)
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserOptionsView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, id):        
        try:
            user = User.objects.get(id=id)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:                
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data)

            if not serializer.is_valid():
                print(serializer.errors)
                return Response({"Erro na requisição"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({'Usuário excluído com sucesso'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        



    

