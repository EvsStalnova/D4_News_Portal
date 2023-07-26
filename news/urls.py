from django.urls import path
from . import views
from .views import NewsList, NewsDetail, Search, NewsEdit, NewsDelete, ArticleCreate, ArticleEdit, ArticleDelete

app_name = 'news'

urlpatterns = [
    path('', views.Start_Padge, name='Start'),  # URL-шаблон Стартовой страницы
    path('search/', Search.as_view(), name='search'),  # URL-шаблон Поисковой страницы
    path('news/', NewsList.as_view(), name='news_list'),  # URL-шаблон для списка новостей
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('article/', views.article_list, name='article_list'),  # URL-шаблон для списка статей
    path('<int:post_id>/', views.article_detail, name='article_detail'),
    path('news/create/', views.NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]