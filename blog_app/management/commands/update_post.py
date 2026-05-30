from django.core.management import BaseCommand

from blog_app.models import Post


class Command(BaseCommand):
    help = "Обновление статьи"

    def add_arguments(self, parser):
        parser.add_argument("id", type=int, help="ID статьи")
        parser.add_argument("-t", "--title", type=str, help="Название статьи")

    def handle(self, *args, **options):
        post_id = options["id"]
        new_title = options["title"]

        try:
            post = Post.objects.get(id=post_id)
            post.title = new_title
            post.save()
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR("Пост не найден"))
