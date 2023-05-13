from django.db import models
from django.contrib.auth.models import User

class RecipeCategory(models.Model):
	cuisine = models.CharField(max_length=128)
	def __str__(self):
		return self.cuisine

class RecipeEntry(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    ingredients=models.CharField(max_length=1000)
    recipe_id = models.CharField(max_length=3,unique=True)
    display_picture = models.ImageField(blank=True, null=True, upload_to="")

class RecipeReview(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)  
   recipe_id = models.ForeignKey("RecipeEntry",on_delete=models.CASCADE)
   review_text=models.TextField()
   review_rating = models.IntegerField(default=0)

class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    recipe_id = models.ForeignKey("RecipeEntry",on_delete=models.CASCADE)

class ShoppingList(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    ingredients=models.CharField(max_length=1000)