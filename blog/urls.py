from django.urls import path

from . import views
from .views import *
from .feeds import LatestPostsFeed
app_name = 'blog'
urlpatterns = [
    path('post/', post_list, name='post_list'),
    # path('', PostListView.as_view()),
    path('tag/<slug:tag_slug>/',
         views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('<int:post_id>/comment/', post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed')
]
