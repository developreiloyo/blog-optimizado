from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count']
        
    def get_posts_count(self, obj):
        return obj.post_set.count()

class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    content_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'category', 
            'content_preview', 'image', 'created_at', 'updated_at'
        ]
        
    def get_content_preview(self, obj):
        # Devuelve los primeros 150 caracteres del contenido
        return obj.content[:150] + '...' if len(obj.content) > 150 else obj.content

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'author', 
            'category', 'image', 'created_at', 'updated_at'
        ]

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']
        
    def create(self, validated_data):
        # El autor se asigna automáticamente desde el request
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)