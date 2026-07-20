from django.contrib.auth.models import User
from ninja import Router
from ninja.errors import HttpError
from slugify import slugify

from blog_app.models import Post, Category
from feedback_app.models import Feedback
from ninja_app.schemas import (
    PostOutSchema, PostInSchema, CategoryOutSchema, CategoryInSchema, FeedbackOutSchema,
    FeedbackInSchema
)

router = Router()


@router.get(path="/ping")
def ping(request):
    return {"pong": True}


@router.get(path="/posts", response=list[PostOutSchema])
async def list_posts(request, search: str | None = None, category_id: int | None = None):
    query_set = Post.objects.filter(published=True)

    if search:
        query_set = query_set.filter(title__icontains=search)

    if category_id:
        query_set = query_set.filter(category_id=category_id)

    posts = [post async for post in query_set]

    return posts


@router.get(path="/posts/{post_id}", response=PostOutSchema)
async def get_post(request, post_id: int):
    try:
        post = await Post.objects.aget(pk=post_id)
        return post
    except Post.DoesNotExist:
        raise HttpError(status_code=404, message="Статья не найдена")


@router.post(path="/posts", response={201: PostOutSchema})
async def create_post(request, payload: PostInSchema):
    post_data = payload.dict()
    post_data['slug'] = slugify(post_data['title'])
    post_data['author'] = await User.objects.afirst()
    post_data['category_id'] = post_data.pop('category')

    new_post = await Post.objects.acreate(**post_data)
    return 201, new_post


@router.get(path="/categories", response=list[CategoryOutSchema])
async def list_categories(request, search_title: str | None = None):
    query_set = Category.objects.all()

    if search_title:
        query_set = query_set.filter(title__icontains=search_title)

    categories = [category async for category in query_set]

    return categories


@router.get(path="/categories/{category_id}", response=CategoryOutSchema)
async def get_category(request, category_id: int):
    try:
        category = await Category.objects.aget(pk=category_id)
        return category
    except Category.DoesNotExist:
        raise HttpError(status_code=404, message="Категория не найдена")


@router.post(path="/categories", response={201: CategoryOutSchema})
async def create_category(request, payload: CategoryInSchema):
    new_category = await Category.objects.acreate(**payload.dict())
    return 201, new_category


@router.put(path="/categories/{category_id}", response=CategoryOutSchema)
async def update_category(request, category_id: int, payload: CategoryInSchema):
    try:
        await Category.objects.filter(pk=category_id).aupdate(
            title=payload.title,
            slug=payload.slug
        )
        category = await Category.objects.aget(pk=category_id)
        return category
    except Category.DoesNotExist:
        raise HttpError(status_code=404, message="Категория не найдена")


@router.delete(path="/categories/{category_id}", response={204: CategoryOutSchema})
async def delete_category(request, category_id: int):
    try:
        category = await Category.objects.aget(pk=category_id)
        await category.adelete()
        return 204, category
    except Category.DoesNotExist:
        raise HttpError(status_code=404, message="Категория не найдена")


@router.post(path="/feedback", response={201: FeedbackOutSchema})
async def create_feedback(request, payload: FeedbackInSchema):
    new_feedback = await Feedback.objects.acreate(**payload.dict())
    return 201, new_feedback
