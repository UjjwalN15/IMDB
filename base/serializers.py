from rest_framework import serializers
from .models import *

class PlatformSerializer(serializers.ModelSerializer):
    # For Hyperlinked movies
    # movies = serializers.HyperlinkedRelatedField(view_name='movies_detail',  # Name of the view that provides the URL for Movies many=True,read_only=True
    # many=True, read_only=True)
    movies = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Platform
        fields = '__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['movie'] = instance.movie.title if instance.movie else None
        return representation
    class Meta:
        model = Reviews
        fields = ['id','movie', 'email', 'full_name','ratings','comment']
        
    def validate_ratings(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Ratings should be between 1 and 5")
        return value
class MovieSerializer(serializers.ModelSerializer):
    # platform = serializers.StringRelatedField()
    rating = serializers.ReadOnlyField()
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['platform'] = instance.platform.name if instance.platform else None
        return representation
    class Meta:
        model = Movies
        fields = ['id','title','description','rating','release_year','active','platform','added_date','updated_date']
    # platform = PlatformSerializer()
        
