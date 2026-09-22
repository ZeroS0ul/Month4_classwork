from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from posts.forms import CommentForm, PostForm
from posts.models import Category, Post, Tag


class HelloWorldView(View):
    def get(self, request):
        return HttpResponse("<h1>Hello world!</h1>")


class MyNameView(TemplateView):
    def get(self, request, *args, **kwargs):
        name = "Dmitry"
        return HttpResponse(f"<h2>Hello</h2> <h1>{name}</h1>")


class SayNameView(TemplateView):
    def get(self, request, name, *args, **kwargs):
        return HttpResponse(f"<h2>Hello</h2> <h1>{name}</h1>")


class PostListView(ListView):
    model = Post
    template_name = "posts/list_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("search")

        if query:
            query = query.strip()
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(text__icontains=query)
                )

        return queryset


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
    success_url = reverse_lazy("my_posts")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["categories"] = Category.objects.all()
        return context

    def get_form(self, form_class: BaseModelForm | None = None) -> BaseModelForm:
        form = super().get_form(form_class)
        form.instance.user = self.request.user
        return form


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create_post.html"
    success_url = reverse_lazy("my_posts")

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


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("my_posts")

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.user != self.request.user:
            raise PermissionDenied
        return object


class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/my_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)