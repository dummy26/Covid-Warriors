from django.contrib import admin
from django.urls import path, include
from .import views
from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('', ArticleListView.as_view(), name='homepage'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('live_tracker', views.live_tracker, name='live_tracker'),
    path('search', views.search, name='search'),
    # path('search_tab', views.search_tab, name='search_tab')


]
