# blog/api_urls.py

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .api_views import (
    PostListAPIView, PostDetailAPIView, PostCreateAPIView, 
    PostUpdateAPIView, PostDeleteAPIView,
    CategoryListAPIView, CategoryDetailAPIView, CategoryPostsAPIView,
)

app_name = 'blog_api'

urlpatterns = [
    # JWT Authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Posts endpoints
    path('posts/', PostListAPIView.as_view(), name='post_list'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post_create'),
    path('posts/<slug:slug>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/update/', PostUpdateAPIView.as_view(), name='post_update'),
    path('posts/<slug:slug>/delete/', PostDeleteAPIView.as_view(), name='post_delete'),
    
    # Categories endpoints
    path('categories/', CategoryListAPIView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('categories/<slug:slug>/posts/', CategoryPostsAPIView.as_view(), name='category_posts'),
]