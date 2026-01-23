from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post
from comments.models import Comment


def post_list(request):
    posts = Post.objects.filter(status="published").order_by("-created_at")
    return render(request, "posts/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status="published")
    comments = post.comments.all().order_by("-created_at")
    return render(
        request, "posts/post_detail.html", {"post": post, "comments": comments}
    )


@login_required
def post_create(request):
    if request.method == "POST":
        Post.objects.create(
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            status=request.POST.get("status"),
            author=request.user,
        )
        return redirect("posts:post_list")
    return render(request, "posts/post_form.html")


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.status = request.POST.get("status")
        post.save()
        return redirect("posts:post_detail", pk=post.pk)
    return render(request, "posts/post_form.html", {"post": post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        post.delete()
        return redirect("posts:post_list")
    return render(request, "posts/post_confirm_delete.html", {"post": post})
