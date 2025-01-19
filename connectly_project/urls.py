from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('api-auth/', include('rest_framework.urls')),  # API authentication
    path('posts/', include('blog_posts.urls')),  # Routes for blog_posts app
    path('', home, name='home'),  # Root URL
]
