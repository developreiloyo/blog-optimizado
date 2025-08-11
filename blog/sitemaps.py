# blog/sitemaps.py
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.db.models import Max
from .models import Post, Category


class BaseHTTPSitemap(Sitemap):
    """
    Fuerza http en modo DEBUG y https en producción.
    """
    protocol = "http" if settings.DEBUG else "https"


class StaticViewSitemap(BaseHTTPSitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        # Rutas estáticas y home (ajusta si cambian los names)
        return ["blog:post_list", "blog:about", "blog:contact"]

    def location(self, item):
        return reverse(item)


class PostSitemap(BaseHTTPSitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        # Solo posts publicados
        return Post.objects.filter(status="published")

    def lastmod(self, obj: Post):
        return obj.updated_at

    def location(self, obj: Post):
        # Depende de get_absolute_url() en tu modelo
        return obj.get_absolute_url()


class CategorySitemap(BaseHTTPSitemap):
    changefreq = "weekly"
    priority = 0.3

    def items(self):
        # Categorías que tienen al menos un post publicado
        return Category.objects.filter(post__status="published").distinct()

    def lastmod(self, obj: Category):
        # Última actualización entre los posts de la categoría
        return (
            Post.objects.filter(category=obj, status="published")
            .aggregate(m=Max("updated_at"))["m"]
        )

    def location(self, obj: Category):
        return obj.get_absolute_url()
