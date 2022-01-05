from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import User, Music, Movie
from .serializers import MusicSerializer, MovieSerializer


class AuthenticationApiView(APIView):

    def post(self, request):
        try:
            user = User.objects.get(email=request.data["email"])
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "success": True,
                "email": user.email,
                "token": token.key
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)


class MultiMediaApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        music_qs = Music.objects.all()
        movie_qs = Movie.objects.all()
        if music_qs.exists() and movie_qs.exists():
            music_serializer = MusicSerializer(music_qs, many=True)
            movie_serializer = MovieSerializer(movie_qs, many=True)
            return Response({
                "success": True,
                "music": music_serializer.data,
                "movie": movie_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "music": [],
                "movie": []
            }, status=status.HTTP_404_NOT_FOUND)