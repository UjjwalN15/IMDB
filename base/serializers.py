from rest_framework import serializers
from .models import *

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['platform'] = instance.platform.name if instance.platform else None
        return representation
    class Meta:
        model = Movies
        fields = '__all__'
    # platform = PlatformSerializer()
        
class ReviewSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['movie'] = instance.movie.title if instance.movie else None
        return representation
    ratings = serializers.FloatField()
    # movie = MovieSerializer()
    class Meta:
        model = Reviews
        fields = '__all__'
        
    def validate_ratings(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Ratings should be between 1 and 5")
        return value