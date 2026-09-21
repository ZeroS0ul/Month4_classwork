"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from posts.views import (
    CreatePostView,
    EditPostView,
    HelloWorldView,
    MyPostsView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    my_name,
    say_name,
)

from user.views import register


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Простые страницы
    path("hello/", HelloWorldView.as_view()),
    path("name/", my_name),
    path("name/<str:name>", say_name),

    # Посты
    path(
        "",
        PostListView.as_view(),
        name="post_list",
    ),

    path(
        "my-posts/",
        MyPostsView.as_view(),
        name="my_posts",
    ),

    path(
        "post/<int:pk>/",
        PostDetailView.as_view(),
        name="post_detail",
    ),

    path(
        "post/create/",
        CreatePostView.as_view(),
        name="create_post",
    ),

    path(
        "post/<int:pk>/delete/",
        PostDeleteView.as_view(),
        name="post_delete",
    ),

    path(
        "post/<int:pk>/edit/",
        EditPostView.as_view(),
        name="edit_post",
    ),

    # Авторизация
    path(
        "accounts/register/",
        register,
        name="register",
    ),

    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
