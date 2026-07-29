"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ninja import NinjaAPI

from ninja_app import api, auth_routes

ninja_api = NinjaAPI(
    version="2.0.0",
    title="Блог NinjaAPI",
)

ninja_api.add_router("/", api.router)
ninja_api.add_router("/auth", auth_routes.auth_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users_app.urls", namespace="users")),
    path("feedback/", include("feedback_app.urls", namespace="feedback")),
    path('tinymce/', include('tinymce.urls')),
    path("", include("blog_app.urls", namespace="blog")),
    # JWT-аутентификация: получение и обновление токенов
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # API приложения
    path("api/v1/", include("drf_app.urls"), name="drf"),
    path("api/v2/", ninja_api.urls)
] + debug_toolbar_urls()

# Раздача медиафайлов сервером разработки ТОЛЬКО при DEBUG = True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
