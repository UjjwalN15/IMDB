from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('movies/', MoviesApiViewSet.as_view({'get': 'list', 'post':'create'}), name='movies'),
    path('movies/<int:pk>/', MoviesApiViewSet.as_view({'get': 'retrieve', 'put':'update','patch': 'partial_update', 'delete':'destroy'}),name='movies_detail'),
    path('platform/', PlatformApiViewSet.as_view({'get': 'list', 'post':'create'}), name='platform'),
    path('platform/<int:pk>/', PlatformApiViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}), name='platform_detail'),
    path('reviews/', ReviewsApiViewSet.as_view({'get': 'list', 'post':'create'}), name='reviews'),
    path('reviews/<int:pk>/', ReviewsApiViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}), name='reviews_detail'),
]