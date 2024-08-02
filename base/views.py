from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
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
