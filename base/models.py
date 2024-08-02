from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
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
    ratings = models.IntegerField(default=5)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Reviews(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=200)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    ratings = models.FloatField()
    comment = models.TextField()
    
    def __str__(self):
        return (self.movie.title + ' => ' + str(self.ratings)+ '  rating')
    
    
