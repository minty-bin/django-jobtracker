from django.urls import path
from .views import (
    UserJobListView,
    JobDetailView,
    JobCreateView,
    JobPostView,
    JobDeleteView,
    PostListView,
    PostCreateView,
    PostPostView,
    PostDetailView,
    PostDeleteView
)
from . import views

urlpatterns = [
    path('', UserJobListView.as_view(), name='jobtracker-home'),
    path('job/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('job/new/', JobCreateView.as_view(), name='job-create'),
    path('job/<int:pk>/post/', JobPostView.as_view(), name='job-post'),
    path('job/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    path('post/<int:pk>/', PostListView.as_view(), name='post-list'),
    path('post/new/<int:pk>/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:jobid>,<int:pk>/post/', PostPostView.as_view(), name='post-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:jobid>,<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='jobtracker-about'),
]