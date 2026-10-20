from django.urls import path 
from . import views 
urlpatterns =[
    path('', views.inicio, name="hola"),
    path('historia/', views.historia, name="historia"),
    path('personajes/', views.personajes, name="personajes"),
    path('descarga/', views.descarga, name="descarga")
]