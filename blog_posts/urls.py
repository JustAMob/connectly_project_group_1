from django.http import HttpResponse
from django.urls import path
from . import views
from .views import UserListCreate, PostListCreate, CommentListCreate
urlpatterns = [
    path('', lambda request: HttpResponse("Welcome to the Posts Home Page!"), name='posts_home'),  # Default view
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('users/create/', views.update_user, name='update_user'),
    path('users/', views.delete_user, name='delete_users'),
]
