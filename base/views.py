from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework import generics
# Create your views here.

class MoviesApiViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movies.objects.all()
    
class PlatformApiViewSet(viewsets.ModelViewSet):
    serializer_class = PlatformSerializer
    queryset = Platform.objects.all()
    
class ReviewsApiViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Reviews.objects.all()
    
class ReviewsApiViewSetDetails(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        movie_id = self.kwargs['pk']
        return Reviews.objects.filter(movie_id=movie_id)
