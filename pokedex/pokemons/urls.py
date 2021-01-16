from django.contrib import admin
from django.urls import path
from pokemons import views

urlpatterns = [
    path('', views.index,name='home'),
    path('poke/<str:pk>/', views.pokemon,name='pokemon'),
    path('pk/', views.search,name='search'),
    path('tp/<str:tk>/', views.typepk,name='typepk'),
    
]
