from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Comment
from posts.models import Post

@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id, status='published')
    if request.method == 'POST':
        Comment.objects.create(
            text=request.POST.get('text'),
            author=request.user,
            post=post
        )
    return redirect('post_detail', pk=post.pk)

@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        comment.text = request.POST.get('text')
        comment.save()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden()
    post_id = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_id)
