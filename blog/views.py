from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render
from taggit.models import Tag
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank
from .forms import SearchForm

# class PostListView(ListView):
#     """
#     Muqobil post ro‘yxati ko‘rinishi
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'list.html'


def post_list(request, tag_slug=None):
    post_lists = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_lists = post_lists.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_lists, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'list.html',
                  {'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # list of active comments for this post
    comments = post.comments.filter(active=True)
    # form for users to comment
    form = CommentForm()
    # list of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'detail.html', {'post': post,
                                           'comments': comments,
                                           'form': form,
                                           'similar_posts': similar_posts})


def post_share(request, post_id):
    # post id ni olish
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # forma yuborish
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form maydonlari validatsiyadan o'tdi
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}sizga {post.title} ni o'qishni tavsiya etadi"
            message = f"{cd['name']}ning izohlari {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post, 'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # create comment objects without saving it to the database
        comment = form.save(commit=False)
        # Assing the post to the comment
        comment.post = post
        # saving the comment to the database
        comment.save()
    return render(request, 'comment.html', {'post': post, 'form': form, 'comment': comment})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(query)
        results = Post.published.annotate(
        search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
    return render(request,
    'search.html',
    {'form': form,
    'query': query,
    'results': results})