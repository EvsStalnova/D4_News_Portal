from django.urls import path
from . import views
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostCreate, PostEdit, PostDelete, Search, ArticleCreate, ArticleDelete, ArticleEdit, upgrade_user

app_name = 'post'

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='post_start'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения,  # URL-шаблон Стартовой страницы
   path('search/', Search.as_view(), name='search'),  # шаблон Поисковой страницы
   path('news/search/', Search.as_view(), name='search_post'),
   path('news/', PostList.as_view(), name='post_list'),  # шаблон для списка новостей
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),  # шаблон для списка новостей
   path('news/create/', PostCreate.as_view(), name='post_create'),  # шаблон для создания новостей
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),  # шаблон для удаления новостей
   path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'), # шаблон для редактирования новостей
   path('article/', views.article_list, name='article_list'),  # URL-шаблон для списка статей
   path('articles/<int:post_id>/', views.article_detail, name='article_detail'),  # шаблон для статьи
   path('articles/create/', ArticleCreate.as_view(), name='articles_create'),  # шаблон для создания статьи
   path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),  # шаблон для редактирования статьи
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),  # шаблон для удаления статьи
   path('upgrade/', upgrade_user, name='account_upgrade')
]