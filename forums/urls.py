from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (ForumCreate, ForumListView, ForumUserListView,  ForumDetailView, ForumUpdateView, ForumDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView)

urlpatterns = [
    path('', ForumListView.as_view(), name='forum-list'),
    path('add/', ForumCreate.as_view(), name='forum-add'),
    path('edit/<int:pk>', ForumUpdateView.as_view(), name='forum-edit'),
    path('delete/<int:pk>', ForumDeleteView.as_view(), name='forum-delete'),
    path('<slug:slug>', ForumDetailView.as_view(), name='forum-detail'),
    path('by/<str:username>/', ForumUserListView.as_view(), name='forum-by'),
    path('add-comment/<int:pk>', CommentCreateView.as_view(), name='add-comment'),
    path('edit-comment/<int:pk>', CommentUpdateView.as_view(), name='edit-comment'),
    path('delete-comment/<int:pk>', CommentDeleteView.as_view(), name='delete-comment'),
    path('search/', views.forum_search, name='forum-search'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)