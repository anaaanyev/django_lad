from django.contrib.auth.models import User
from ninja import Router
from ninja.errors import HttpError
from slugify import slugify

from blog_app.models import Post
from ninja_app.schemas import PostOutSchema, PostInSchema

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
