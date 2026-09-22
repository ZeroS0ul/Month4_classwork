from django.urls import path
from posts.views import (
    CreatePostView,
    EditPostView,
    HelloWorldView,
    MyNameView,
    MyPostsView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    SayNameView,
)

urlpatterns = [
    path("hello/", HelloWorldView.as_view(), name="hello"),
    path("my-name/", MyNameView.as_view(), name="my_name"),
    path("say-name/<str:name>/", SayNameView.as_view(), name="say_name"),
    
    path("", PostListView.as_view(), name="post_list"),
    path("my-posts/", MyPostsView.as_view(), name="my_posts"),
    path("create/", CreatePostView.as_view(), name="create_post"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("<int:pk>/edit/", EditPostView.as_view(), name="edit_post"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
]