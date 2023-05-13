from dataclasses import field
from pyexpat import model
from django import forms
from RecipeManager.models import RecipeEntry, RecipeCategory,RecipeReview

class RecipeForm(forms.ModelForm):
	class Meta():
		model = RecipeEntry
		fields = ('cuisine', 'title', 'description','ingredients', 'recipe_id','display_picture')

class EditForm(forms.ModelForm):
	class Meta():
		model = RecipeEntry
		fields = ('cuisine', 'title', 'description','ingredients','display_picture')

class ReviewForm(forms.ModelForm):
	class Meta():
		model = RecipeReview
		fields = ('review_text', 'review_rating')
		#fields = ('user','book_id', 'review_text', 'review_rating')