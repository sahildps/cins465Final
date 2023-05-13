from django.shortcuts import render
from pickle import TRUE
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from RecipeManager.models import RecipeEntry, RecipeCategory,RecipeReview, Favourites, ShoppingList
from RecipeManager.forms import RecipeForm, EditForm, ReviewForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.
@login_required
def recipes(request):
    if(RecipeCategory.objects.count() == 0):
        RecipeCategory(cuisine = "Indian").save()
        RecipeCategory(cuisine = "Italian").save()
        RecipeCategory(cuisine = "Japanese").save()
        RecipeCategory(cuisine = "Korean").save()
        RecipeCategory(cuisine = "Pakistani").save()
        
        
    else:
        table_data=RecipeEntry.objects.all()
        #table_data = RecipeEntry.objects.filter(user=request.user)
        fav_data = Favourites.objects.filter(user=request.user)
        
        favourites=[]
        for i in fav_data:
            favourites.append(i.recipe_id.recipe_id)
        print(favourites)
        context = {
            "table_data": table_data,
            "favourites":favourites
        }
        return render(request, 'recipes/recipes.html',context)

@user_passes_test(lambda user: user.is_staff)
def add(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            form = RecipeForm(request.POST,request.FILES)
            if (form.is_valid()):
                recipeEntry = form.save(commit=False)
                #bookEntry.user = request.user
                #bookEntry.display_picture = request.FILES['display_picture']
                #print("User:",bookEntry.user)
                recipeEntry.save()
                return redirect("/recipes/")
            else:
                context = {
                    "form_data": form
                }
                return render(request, 'recipes/add.html', context)
        else:
            # Cancel
            return redirect("/recipes/")
    else:
        context = {
            "form_data": RecipeForm()
        }
        
        return render(request, 'recipes/add.html', context)

@user_passes_test(lambda user: user.is_staff)
def edit(request, id):
    if (request.method == "GET"):
        # Load Journal Entry Form with current model data.
        recipeEntry = RecipeEntry.objects.get(id=id)
        print("ed",recipeEntry.recipe_id)
        # data=BookReview.objects.filter(book_id=id)
        # print("data",data)
        #form = BookForm(instance=bookEntry)
        form = EditForm(instance=recipeEntry)
        context = {"form_data": form}
        return render(request, 'recipes/edit.html', context)
    elif (request.method == "POST"):
        # Process form submission
        if ("edit" in request.POST):
            print('Files',request.FILES,'\n')
            #form = BookForm(request.POST)
            form=EditForm(request.POST)
            #print(form)
            if (form.is_valid()):
                recipeEntry = form.save(commit=False)
                #print(bookEntry,id,request.user)
                # bookEntry = BookEntry.objects.get(user=request.user,id=id)
                if bool(request.FILES):					
                    recipeEntry.display_picture = request.FILES['display_picture']	
                    entry=RecipeEntry.objects.get(id=id)
                    recipeEntry.recipe_id=entry.recipe_id
                    print("Edit",entry)
                    #bookEntry.user = request.user
                    print("User")
                    #BookEntry.objects.filter(id=id,user=request.user).update(title=bookEntry.title,author=bookEntry.author,genre=bookEntry.genre,book_id=bookEntry.book_id,display_picture=bookEntry.display_picture)
                    #BookEntry.objects.filter(id=id).update(title=bookEntry.title,author=bookEntry.author,genre=bookEntry.genre,book_id=bookEntry.book_id,display_picture=bookEntry.display_picture)
                    # data=list(BookReview.objects.filter(book_id=id))
                    # print("data",data)
                    
                    delEntry = RecipeEntry.objects.get(id=id)
                    delEntry.delete()

                    recipeEntry.save()
                    # for d in data:
                    #     #print("d",d.book_id) 
                    #     print("d",d.review_text)
                    #     ReviewEntry=BookReview()        
                    #     ReviewEntry.review_text=d.review_text
                    #     ReviewEntry.review_rating=d.review_rating
                    #     ReviewEntry.user=request.user 
                    #     ent = BookEntry.objects.filter(book_id=bookEntry.book_id)[0]
                    #     ReviewEntry.book_id=ent                     
                    #     ReviewEntry.save()
                    

                    #bookEntry = BookEntry.objects.get(id=id)
                    #bookEntry.delete()

                    
                    # pass
                else:
                    #print(BookEntry.objects.filter(id=bookEntry.id,user=request.user))
                    #BookEntry.objects.filter(id=id,user=request.user).update(title=bookEntry.title,author=bookEntry.author,genre=bookEntry.genre,book_id=bookEntry.book_id)
                    RecipeEntry.objects.filter(id=id).update(title=recipeEntry.title,description=recipeEntry.description,cuisine=recipeEntry.cuisine,ingredients=recipeEntry.ingredients)
                return redirect("/recipes/")
            else:
                context = {
                    "form_data": form
                }
                return render(request, 'recipes/edit.html', context)
        else:
            #Cancel
            return redirect("/recipes/")

@user_passes_test(lambda user: user.is_staff)
def delete(request,id):    
    #id = request.GET["delete"]
    RecipeEntry.objects.filter(id=id).delete()
    return redirect("/recipes/")

@login_required
def favourites(request):    
    #table_data=BookEntry.objects.all()
    table_data = Favourites.objects.filter(user=request.user)
    context = {
        "table_data": table_data
    }
    print("context:",context)
    return render(request, 'recipes/favourites.html',context)

@login_required
def addfavourites(request, id):  
    print("here")  
    recipeEntry = RecipeEntry.objects.get(id=id)
    favEntry=Favourites()
    favEntry.user=request.user
    favEntry.recipe_id=recipeEntry
    favEntry.save()
    #return render(request,'books.html')
    return redirect("/recipes")

@login_required
def remfavourites(request,id):  
   #print(id)      
   favEntry=Favourites.objects.filter(recipe_id=id)
   favEntry.delete()
   #return render(request,'books.html')
   return redirect("/recipes")

@login_required
def getshoplist(request):    
    #table_data=BookEntry.objects.all()
    #table_data = ShoppingList.objects.filter(user=request.user)
    shopEntry=ShoppingList.objects.filter(user=request.user)
    table_data=[]
    if shopEntry:
        ingredients=shopEntry[0].ingredients
        table_data=ingredients.split(",")
        
    # for t in table_data:
    #     print(t)
    # print(table_data)
    context = {
        "table_data": table_data
    }
    print("context:",context)
    return render(request, 'recipes/shoppinglist.html',context)

@csrf_exempt
@login_required
def addingreds(request):
    print("in here")
    if (request.method == "POST"):
        data=request.POST
        print("ingred",data)
        values = request.POST.getlist('data[]')
        ingredientslist = ','.join(values)
        print(ingredientslist)
        shopEntry=ShoppingList.objects.filter(user=request.user)
        if shopEntry:
            print("record there")
            ShoppingList.objects.filter(user=request.user).update(ingredients=ingredientslist)
        else:
            shopEntry=ShoppingList()
            shopEntry.user=request.user
            shopEntry.ingredients=ingredientslist
            shopEntry.save()
    # return redirect("/recipes")
    return HttpResponse(200)

def review_list(request,id):
    recipe_data = RecipeEntry.objects.get(id=id)
    print(recipe_data)
    recipe_id=recipe_data.recipe_id
    #book_data=book_data[0]

    data=RecipeReview.objects.filter(recipe_id=id)
    #print("bd",book_data)
    reviewsForm=ReviewForm()
    print("data",data)
    avgrating=0
    totalrating=0
    num=0
    if data:
        for d in data:
            totalrating=totalrating+d.review_rating
            num=num+1
    if num>0:
        avgrating=round(totalrating/num)
    print("avg",avgrating)
    context = {
                    "form_data":data,
                    "recipe_id":recipe_id,                                    
                    "recipe_data":recipe_data,
                    "reviews_form":reviewsForm,
                    "avg_rating":avgrating
                }
    return render(request, 'recipes/reviews.html', context)

@csrf_exempt
def add_review(request,id):
    
    #print("json",json.load(request)['review_text'])
    #print(updatedData)
    print("id",id)
    if (request.method == "POST"):
        print("hey there")        
        #form = ReviewForm(request.POST,request.FILES)
        data=request.POST
        #print(form)
        #if (form.is_valid()):
        #BookReview = form.save(commit=False)
        #  BookReview.review_text=form.review_text
        #  BookReview.review_rating=form.review_rating
        ReviewEntry=RecipeReview()        
        ReviewEntry.review_text=data['review_text']
        ReviewEntry.review_rating=data['review_rating']
        ReviewEntry.user=request.user
        recipeEntry = RecipeEntry.objects.filter(recipe_id=id)[0]
        print("be",recipeEntry)
        ReviewEntry.recipe_id=recipeEntry
        ReviewEntry.save()
        #return redirect("/books/review_list/"+str(id))
        return HttpResponse(200)

