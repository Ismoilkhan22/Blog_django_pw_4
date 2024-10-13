from django.shortcuts import render

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'list.html',
                  {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    return render(request, 'detail.html', {'post': post})























