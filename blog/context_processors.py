from .models import Category

def menu_categories(request):
    categories = Category.objects.filter(parent__isnull=True)
    return {'menu_categories': categories}