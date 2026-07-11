from ninja import ModelSchema
from blog_app.models import Post


class PostOutSchema(ModelSchema):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'category', 'author', 'published', 'created_at')


class PostInSchema(ModelSchema):
    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'published')
