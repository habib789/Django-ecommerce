from django.urls import path
from .views import (PostView, PostDetailView,
                    PostCreate, PostDelete,
                    PostUpdate, add_comment,
                    remove_comment, PostLike, post_searched)

app_name = 'blog'
urlpatterns = [
    path('', PostView.as_view(), name='blog'),
    path('post/create', PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/update', PostUpdate.as_view(), name='post_edit'),
    path('post/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('post/<int:pk>/details', PostDetailView.as_view(), name='post_detail'),
    path('post/post_searched', post_searched, name='post_searched'),
    path('post/<int:pk>/post/comment', add_comment, name='post_comment'),
    path('post/<int:pk>/post/comment/remove', remove_comment, name='comment_remove'),
    path('post/<int:pk>/post/like', PostLike, name='post_like'),
]
