from rest_framework import serializers
from blog_app.models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'category', 'author', 'published', 'created_at')
        read_only_fields = ('id', 'published', 'created_at', 'author', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField(method_name='get_posts_count', read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'posts_count')
        read_only_fields = ('id', 'posts_count')

    def get_posts_count(self, obj):
        return Post.objects.filter(published=True, category=obj).count()
