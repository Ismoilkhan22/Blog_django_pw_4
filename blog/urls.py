from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    # path('post/', post_list, name='post_list'),
    path('post/',PostListView.as_view() ),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
]
