from venv import logger
from django.shortcuts import get_object_or_404, render
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User, Post, Comment, Like
from .serializers import (
    UserSerializer, 
    UserRegisterSerializer, 
    PostSerializer, 
    CommentSerializer,
    UserUpdateSerializer
)
from blog_posts import serializers

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserListView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        # Get all users
        users = User.objects.all()
        
        # Serialize the user data
        user_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        
        return Response(user_data, status=status.HTTP_200_OK)
# Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Like/Unlike a Post
class LikePostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id) 
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({'message': 'Post unliked.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Post liked.'}, status=status.HTTP_201_CREATED)

# Login View using DRF authentication
class LoginView(APIView):
    permission_classes = []
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Register User View
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Token is valid!"})
    
class DeleteAllUsersView(APIView):
    permission_classes = [IsAdminUser]  # Ensure that only admin users can delete users

    def delete(self, request, *args, **kwargs):
        try:
            # Log that the deletion request was received
            logger.info("Delete all users request received")

            # Delete all users except the superuser/admin account
            users_to_delete = User.objects.exclude(is_superuser=True)
            deleted_count, _ = users_to_delete.delete()  # This will delete the users

            # Log how many users were deleted
            logger.info(f"{deleted_count} users deleted successfully.")
            return Response({"message": f"{deleted_count} users deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            # Log the error if an exception occurs
            logger.error(f"Error occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    permission_classes = [IsAdminUser]  # Ensure that only admin users can delete users

    def delete(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)  # Get user by ID
            user.delete()
            return Response({"message": f"User {user.username} deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)



class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can update

    def put(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)  # Get user by ID
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Use the serializer to validate and update the user's data
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()  # Save the updated user
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)