from django.contrib import admin
from django.urls import path, include
from .import views
from .views import ArticleListView, ArticleDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # change when homepage ready 
    path('', views.homepage, name='homepage'),
    # change when article tab ready 
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('india_tracker', views.india_tracker, name='india_tracker'),
    path('search', views.search, name='search'),
    path('world_tracker', views.world_tracker, name='world_tracker'),
    path('search_tab', views.search_tab, name='search_tab'),
    path('404', views.page404, name='404'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
