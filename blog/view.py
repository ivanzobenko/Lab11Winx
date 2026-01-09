from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone

from .models import Post, Comment
from .forms import PostForm, CommentForm

# Список постов
def post_list(request):
    posts = Post.objects.filter(status="published")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": CommentForm()
    })
@login_required
def post_create(request):
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.created_at = timezone.now()
        post.save()
        return redirect("post_list")

    return render(request, "blog/post_form.html", {"form": form})
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden()

    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect("post_list")

    return render(request, "blog/post_form.html", {"form": form})
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author == request.user:
        post.delete()

    return redirect("post_list")
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.created_at = timezone.now()
        comment.save()

    return redirect("post_detail", post_id=post.id)