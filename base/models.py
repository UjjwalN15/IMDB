from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models import Avg
# Create your models here.

class Platform(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    
    def __str__(self):
        return self.name
    

class Movies(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.DateField()
    active = models.BooleanField(default=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='movies')
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    @property
    def rating(self):
        avg_rating = self.reviews.aggregate(average=Avg('ratings'))['average']
        return avg_rating if avg_rating is not None else 0
    
class Reviews(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=200)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='reviews')
    ratings = models.FloatField()
    comment = models.TextField()
    
    def __str__(self):
        return (self.movie.title + ' => ' + str(self.ratings)+ '  rating')
    
    
