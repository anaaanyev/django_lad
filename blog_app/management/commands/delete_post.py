from django.core.management import BaseCommand
from blog_app.models import Post

class Command(BaseCommand):
    help = "Удаление статьи"

    def add_arguments(self, parser):
        parser.add_argument("id", type=int, help="ID статьи")

    def handle(self, *args, **options):
        post_id = options["id"]

        try:
            Post.objects.filter(id=post_id).delete()
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR("Пост не найден"))
