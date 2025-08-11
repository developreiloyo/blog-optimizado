from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.urls import re_path
from django.contrib.sitemaps.views import index, sitemap
from blog.sitemaps import StaticViewSitemap, PostSitemap, CategorySitemap

sitemaps = {
    "static": StaticViewSitemap,
    "posts": PostSitemap,
    "categories": CategorySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    path("api/", include("blog.api_urls", namespace="blog_api")),
    path("robots.txt", include("robots.urls")),

    # Índice y secciones:
    path(
        "sitemap.xml",
        index,
        {"sitemaps": sitemaps, "sitemap_url_name": "sitemap-section"},  # <-- añadido
    ),
    path(
        "sitemap-<section>.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap-section",
    ),
]

urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]


