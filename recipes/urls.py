"""recipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views as core_views
from RecipeManager import views as recipe_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name = 'home'),    
    path('join/', core_views.join),
    path('login/', core_views.user_login),
    path('logout/', core_views.user_logout),
    path('about/', core_views.about),
    path('recipes/', recipe_views.recipes),
    path('recipes/add/', recipe_views.add),
    path('recipes/edit/<int:id>/', recipe_views.edit),
    path('recipes/delete/<int:id>/', recipe_views.delete),
    path('favourites/', recipe_views.favourites),
    path('recipes/addfavourites/<int:id>/', recipe_views.addfavourites),
    path('recipes/remfavourites/<int:id>/', recipe_views.remfavourites),
    path('getshoplist/', recipe_views.getshoplist),
    path('recipes/addingreds/',recipe_views.addingreds),
    path('recipes/review_list/<int:id>/', recipe_views.review_list),
    path('recipes/add_review/<int:id>/', recipe_views.add_review)
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
