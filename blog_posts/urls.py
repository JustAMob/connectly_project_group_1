from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeleteAllUsersView, DeleteUserView, LoginView, RegisterView, TestTokenView, UpdateUserView, UserListView, UserViewSet, PostViewSet, CommentViewSet, LikePostView

# Set up the Default Router to handle standard CRUD routes for User, Post, and Comment
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    # Include automatically generated routes from the router
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('test/', TestTokenView.as_view(), name='test'),
    path('delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
    path('update-user/<int:pk>/', UpdateUserView.as_view(), name='update-user'),
    path('delete-all-users/', DeleteAllUsersView.as_view(), name='delete-all-users'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    # Custom route for liking/unliking posts
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
]
