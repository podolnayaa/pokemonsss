"""
URL configuration for poke project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from quickstart import views

poke_patterns = [
    path("", views.show_pokemon, name='show_pokemon'),
    path("fight/", views.poke_fights, name='poke_fights'),
    path("fast_fight/", views.poke_fast_fight, name='poke_fast_fight'),

    path("save_info/", views.poke_save_info, name='poke_save_info'),

]

urlpatterns = [
    path("", views.index, name='home'),
    path("search_pokemon/", views.search_pokemon, name='search_pokemon'),
    path("pokemon/<str:name>/", include(poke_patterns)),
]