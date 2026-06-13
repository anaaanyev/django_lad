from slugify import slugify
from django.core.management import BaseCommand
from blog_app.models import Post


class Command(BaseCommand):
    help = "Создание статьи"

    def add_arguments(self, parser):
        parser.add_argument("-t", "--title", type=str, help="Название статьи")
        parser.add_argument("-c", "--content", type=str, help="Содержимое статьи")

    def handle(self, *args, **options):
        Post.objects.create(
            title=options["title"],
            slug=slugify(options["title"]),
            content=options["content"],
            author_id=1,  # заглушка, чтобы не было ошибки
            category_id=1,  # заглушка
        )
