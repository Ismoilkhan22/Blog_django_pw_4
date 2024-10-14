from django.shortcuts import render

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage

from .forms import EmailPostForm
from .models import Post

from django.views.generic import ListView


class PostListView(ListView):
    """
    Muqobil post ro‘yxati ko‘rinishi
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'list.html'


# def post_list(request):
#     post_lists = Post.published.all()
#     # Pagination with 3 posts per page
#     paginator = Paginator(post_lists, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'list.html',
#                   {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'detail.html', {'post': post})


def post_share(request, post_id):
    # post id ni olish
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # forma yuborish
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # forma maydonlari validatsiyadan o'tdi
            cd = form.cleaned_data
            # ...elektron pochtaga junatish
    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post, 'form': form})
