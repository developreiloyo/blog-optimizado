# blog/api_views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters

from .models import Post, Category
from .serializers import (
    PostListSerializer, 
    PostDetailSerializer, 
    PostCreateUpdateSerializer,
    CategorySerializer, 
    UserSerializer
)

# Vistas de Posts
class PostListAPIView(generics.ListAPIView):
    """
    Lista todos los posts publicados
    Permite filtrado y búsqueda
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

class PostDetailAPIView(generics.RetrieveAPIView):
    """
    Detalle de un post específico
    """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]  # Público
    lookup_field = 'slug'

class PostCreateAPIView(generics.CreateAPIView):
    """
    Crear un nuevo post (requiere autenticación)
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        excerpt = self.request.data.get("excerpt")
        content = self.request.data.get("content")

        if not excerpt and content:
            excerpt = content[:200]  # autogenerar si no lo mandan

        serializer.save(author=self.request.user, excerpt=excerpt)

class PostUpdateAPIView(generics.UpdateAPIView):
    """
    Actualizar un post existente (solo el autor)
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def get_queryset(self):
        # Solo permite editar sus propios posts
        return Post.objects.filter(author=self.request.user)

class PostDeleteAPIView(generics.DestroyAPIView):
    """
    Eliminar un post (solo el autor)
    """
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def get_queryset(self):
        # Solo permite eliminar sus propios posts
        return Post.objects.filter(author=self.request.user)

# Vistas de Categorías
class CategoryListAPIView(generics.ListAPIView):
    """
    Lista todas las categorías
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryDetailAPIView(generics.RetrieveAPIView):
    """
    Detalle de una categoría específica
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class CategoryPostsAPIView(generics.ListAPIView):
    """
    Posts de una categoría específica
    """
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Post.objects.filter(category__slug=category_slug).order_by('-created_at')