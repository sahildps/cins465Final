from django.contrib import admin
from .models import RecipeCategory,RecipeEntry,RecipeReview,Favourites,ShoppingList

admin.site.register(RecipeCategory)
admin.site.register(RecipeEntry)
admin.site.register(Favourites)
admin.site.register(ShoppingList)
admin.site.register(RecipeReview)
