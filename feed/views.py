from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post, Like, Comment
from django.contrib.auth.models import User

from .forms import PostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from django.views.generic.base import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class HomeView(TemplateView):
    template_name = "feed/home.html"


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("home")


class DeletePostView(DeleteView):
    model = Post
    success_url = reverse_lazy("home")


class ListPostView(ListView):
    model = Post
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all post IDs
        post_ids = [post.id for post in context["posts"]]

        # Get the count of likes for each post by the current user
        user_likes = Like.objects.filter(post__in=post_ids, user=self.request.user)
        users_likes = Like.objects.filter(
            post__in=post_ids, user=self.request.user
        ).exists()
        context["users_likes"] = users_likes
        post_likes_dict = (
            user_likes.values("post")
            .annotate(like_count=Count("post"))
            .values("post", "like_count")
        )

        # Create a dictionary mapping post IDs to like counts
        post_likes_dict = {like["post"]: like["like_count"] for like in post_likes_dict}

        # Update the context with like counts for each post
        for post in context["posts"]:
            post.like_count = post_likes_dict.get(post.id, 0)

        return context


class LikeFormView(View):
    model = Like
    fields = []

    def post(self, request, *args, **kwargs):
        user = self.request.user
        post_pk = self.kwargs.get("post_pk")

        post = Post.objects.get(pk=post_pk)

        if Like.objects.filter(user=user, post=post).exists():
            Like.objects.filter(user=user, post=post).delete()
        else:
            Like.objects.create(user=user, post=post)

        return redirect("list")


class CommentFormView(CreateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy("list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = self.request.user
        post_pk = self.kwargs.get("post_pk")
        post = Post.objects.get(pk=post_pk)

        form = CommentForm(self.request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.post = post
            comment.save()
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    form_class = PostForm
    context_object_name = "post"



