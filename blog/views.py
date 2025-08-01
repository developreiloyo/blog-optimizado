from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Category

# Vista de índice (puedes mostrar destacados o todas las categorías)
from django.shortcuts import render
from .models import Post, Category

def post_list(request):
    # Categoría 1: Crecimiento Personal
    crecimiento = Category.objects.filter(slug="crecimiento").first()
    crecimiento_posts = Post.objects.filter(category=crecimiento, status="published")

    # Categoría 2: Automatización
    automatizacion = Category.objects.filter(slug="automatizacion").first()
    automatizacion_posts = Post.objects.filter(category=automatizacion, status="published")

    # Categoría 3: Portugués
    portugues = Category.objects.filter(slug="portugues").first()
    portugues_posts = Post.objects.filter(category=portugues, status="published")

    # Categoria 4: ingles
    ingles = Category.objects.filter(slug="ingles").first()
    ingles_posts = Post.objects.filter(category=ingles, status="published")

    return render(request, "blog/index.html", {
        "crecimiento": crecimiento,
        "crecimiento_posts": crecimiento_posts,
        "automatizacion": automatizacion,
        "automatizacion_posts": automatizacion_posts,
        "portugues": portugues,
        "portugues_posts": portugues_posts,
        "ingles": ingles,
        "ingles_posts": ingles_posts,
    })

# Vista para mostrar posts por categoría con paginación
def category_posts(request, slug):
    """Vista para mostrar todos los posts de una categoría específica"""
    category = get_object_or_404(Category, slug=slug)
    
    # Obtener todos los posts de la categoría con status consistente
    posts_list = Post.objects.filter(
        category=category, 
        status="published"   # 👈 corregido
    ).order_by('-created_at')
    
    # Configurar paginación
    paginator = Paginator(posts_list, 4)  # 12 posts por página
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, "blog/categoria.html", {
        "category": category,
        "posts": posts,        # Page object para iterar en el template
        "posts_list": posts_list,  # QuerySet completo si lo necesitas
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    
    # Posts recientes para mostrar en la barra lateral
    recent_posts = Post.objects.filter(status='published').exclude(id=post.id).order_by('-created_at')[:5]
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
    }
    
    return render(request, 'blog/post_detail.html', context)

