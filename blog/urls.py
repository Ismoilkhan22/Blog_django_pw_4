from django.urls import path
from .views import *

urlpatterns = [
    path('post/list', post_list, name='post-list'),
    path('post/detail/<int:pk>/',post_detail, name='post-detail'),
]
