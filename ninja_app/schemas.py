from datetime import datetime
from typing import Literal

from ninja import ModelSchema, Schema
from blog_app.models import Post, Category
from pydantic import Field, EmailStr


class PostOutSchema(ModelSchema):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'category', 'author', 'published', 'created_at')


class PostInSchema(ModelSchema):
    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'published')


class CategoryOutSchema(ModelSchema):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')


class CategoryInSchema(ModelSchema):
    class Meta:
        model = Category
        fields = ('title', 'slug')


class FeedbackOutSchema(Schema):
    id: int
    name: str
    email: str
    message: str
    created_at: datetime
    subject: str


class FeedbackInSchema(Schema):
    name: str = Field(max_length=10)
    email: EmailStr
    message: str
    subject: Literal['default', 'tech', 'collaboration', 'complaint', 'other']


class PostSearchResultSchema(Schema):
    id: int
    title: str
    slug: str
    headline: str
    rank: float
