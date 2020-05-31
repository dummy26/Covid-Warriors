from django.contrib import admin
from django.urls import path, include
from .import views
from .views import ArticleListView, ArticleDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # change when homepage ready 
    path('', ArticleListView.as_view(), name='homepage'),
    # change when article tab ready 
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('live_tracker', views.live_tracker, name='live_tracker'),
    path('search', views.search, name='search'),
    # path('search_tab', views.search_tab, name='search_tab')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
