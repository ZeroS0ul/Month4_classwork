from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.db.models.base import Model
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from posts.forms import CommentForm, PostForm
from posts.models import Category, Post, Tag


class HelloWorldView(View):
    def get(self, r):
        return HttpResponse("<h1>Hello world!</h1>")

    def post(self, r):
        ...


def my_name(r):
    name = "Dmitry"

    return HttpResponse(
        f"<h2>Hello</h2> <h1>{name}</h1>"
    )


def say_name(r, name):
    return HttpResponse(
        f"<h2>Hello</h2> <h1>{name}</h1>"
    )


class PostListView(ListView):
    model = Post
    template_name = "posts/list_posts.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"

    def get_object(self, queryset=None):
        object = super().get_object(queryset)

        object.views += 1
        object.save()

        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.all()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()

            return self.get(request, *args, **kwargs)

        context = self.get_context_data()
        context["comment_form"] = form

        return self.render_to_response(context)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create_post.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["tags"] = Tag.objects.all()
        context["categories"] = Category.objects.all()

        return context

    def get_form(
        self,
        form_class: BaseModelForm | None = None,
    ) -> BaseModelForm:
        form = super().get_form(form_class)

        form.instance.user = self.request.user

        return form


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("post_list")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)

        if object.user != self.request.user:
            raise PermissionDenied

        return object


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "posts/edit_post.html"
    form_class = PostForm

    def get_object(self, queryset=None):
        object = super().get_object(queryset)

        if object.user != self.request.user:
            raise PermissionDenied

        return object

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["tags"] = Tag.objects.all()
        context["categories"] = Category.objects.all()

        return context

class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/my_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(
            user=self.request.user
        )
