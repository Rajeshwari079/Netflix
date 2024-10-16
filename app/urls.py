from django.urls import path
from .views import *
app_name='app'

urlpatterns = [
    path('signup/',signup,name='signup'),
    path('',userlogin,name='userlogin'),
    path('index/',index,name='index'),
    path('movie/<str:pk>',movie,name='movie'),
    path('logout/',logout,name='logout'),
    path('search/',search,name='search'),
    path('my_list/',my_list,name='my_list'),
    path('genre/<str:pk>',genre,name='genre'),
    path('movie/<str:pk>',movie,name='movie'),
    path('add_to_list/',add_to_list,name='add_to_list')
]