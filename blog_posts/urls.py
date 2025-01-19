from django.http import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda request: HttpResponse("Welcome to the Posts Home Page!"), name='posts_home'),  # Default view
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('posts/', views.get_posts, name='get_posts'),
    path('posts/create/', views.create_post, name='create_post'),
]
