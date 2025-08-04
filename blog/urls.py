from django.urls import path
from .views import post_list, category_posts, post_detail, about

app_name = "blog"

urlpatterns = [
    path('', post_list, name="post_list"),
    path('post/<slug:slug>/', post_detail, name="post_detail"),
    path('categoria/<slug:slug>/', category_posts, name="category_posts"),
    path('about/', about, name="about"), 
]
