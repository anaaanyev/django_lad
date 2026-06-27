from blog_app.models import Category


def categories_processors(request):
    return {'nav_categories': Category.objects.all()}
