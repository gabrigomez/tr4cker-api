from .models import User, Artist
from .serializers import UserSerializer, RegisterUserSerializer, MyTokenObtainPairSerializer, ArtistSerializer

from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .utils import get_token, search_artist, get_songs, search_artist_by_id

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
        
class CreateArtistView(generics.CreateAPIView):
    serializer_class = ArtistSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            image = serializer.data.get('image')
            genre = serializer.data.get('genre')
            user_id = serializer.data.get('user')
            spotify_id = serializer.data.get('spotify_id')
                        
            user = User.objects.get(id=user_id)
            artist = Artist(name=name, image=image, genre=genre, user=user, spotify_id=spotify_id)
            
            artist.save()
            return Response(ArtistSerializer(artist).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class ArtistOptionsView(generics.CreateAPIView):
    serializer_class = ArtistSerializer
    
    def get(self, request, id):
        try:
            artist = Artist.objects.get(id=id)            
            if not artist:
                return Response({'Artista não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            return Response(ArtistSerializer(artist).data, status=status.HTTP_200_OK)
        except:
            return Response({'Ocorreu um erro na requisição'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        try:
            artist = Artist.objects.get(id=id)
            artist.delete()
            return Response({'Artista excluído com sucesso'}, status=status.HTTP_200_OK)
        except Artist.DoesNotExist:
            return Response({'Artista não encontrado'}, status=status.HTTP_404_NOT_FOUND)

class ArtistListView(generics.CreateAPIView):
    serializer_class = ArtistSerializer
    
    def get(self, request, id):
        try:
            artists = Artist.objects.filter(user_id=id).values()
            if not artists:
                return Response({'Artista não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            return Response(artists, status=status.HTTP_200_OK)
        except:
            return Response({'Ocorreu um erro na requisição'}, status=status.HTTP_404_NOT_FOUND)   

            
        
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
        
class SpotifyArtistSearchView(generics.ListAPIView):
    def post(self, request):
        artist = request.data["artist"]
        limit = request.data["limit"]        
        token = get_token()
        result = search_artist(token, artist, limit)

        if result:
            response_data = []  # List to store individual artist

            for artist_info in result:
                artist_id = artist_info["id"]
                songs = get_songs(token, artist_id)
                
                artist_data = {
                    "name": artist_info["name"],
                    "spotify_id": artist_id,
                    "followers": artist_info["followers"]["total"],
                    "genre": artist_info["genres"][0] if artist_info["genres"] else "",
                    "external_url": artist_info["external_urls"]["spotify"],
                    "image": artist_info["images"][0]["url"] if artist_info["images"] else "", # Check if artist has an image
                    "songs": [song["name"] for song in songs]
                }
                
                response_data.append(artist_data)
                
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Nenhum artista encontrado"}, status=status.HTTP_404_NOT_FOUND)

class SpotifyArtistSearchByIdView(generics.ListAPIView):
    def post(self, request):
        id = request.data["id"]                
        token = get_token()
        result = search_artist_by_id(token, id)

        if result:            
            artist_id = result["id"]
            songs = get_songs(token, artist_id)
            
            artist_data = {
                "name": result["name"],
                "spotify_id": artist_id,
                "followers": result["followers"]["total"],
                "genre": result["genres"][0] if result["genres"] else "",
                "external_url": result["external_urls"]["spotify"],
                "image": result["images"][0]["url"] if result["images"] else "", # Check if artist has an image
                "songs": [song["name"] for song in songs]
            }                
            return Response(artist_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Nenhum artista encontrado"}, status=status.HTTP_404_NOT_FOUND)
          
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
        



    

