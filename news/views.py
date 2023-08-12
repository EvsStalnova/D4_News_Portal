# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm, ArticleForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group


@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('post:post_list')


class PostList(ListView):
    paginate_by = 10
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    # queryset = Product.objects.ffilters().order_by() если нужно задать условие
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'postt.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'postt'

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset().filter(post_type='news')
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        # Возвращаем из функции отфильтрованный список товаров
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    # def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        # context = super().get_context_data(**kwargs)
        # # К словарю добавим текущую дату в ключ 'time_now'.
        # # context['time_now'] = datetime.utcnow()
        # # # Добавим ещё одну пустую переменную,
        # # # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # # context['next_sale'] = 'Распродажа в среду'
        # context['filterset'] = self.filterset
        # return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newPortal.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('post:post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        post.author = self.request.user.author
        post.save()
        return super().form_valid(form)


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newPortal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post:post_list')


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newPortal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post:post_list')


def article_list(request):
    article = Post.objects.filter(post_type='post').order_by('-created_at')  # Фильтруем только статьи
    # и сортируем по убыванию даты
    paginator = Paginator(article, 2)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'article_list.html', {'articles': articles})


def article_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'article_detail.html', {'post': post})


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newPortal.add_post',)
    model = Post
    form_class = ArticleForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('post:article_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        post.author = self.request.user.author
        post.save()
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newPortal.change_post',)
    model = Post
    form_class = ArticleForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('post:article_list')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newPortal.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post:article_list')


class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    filterset_class = PostFilter
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['categories'] = Category.objects.all()  # Получение всех категорий
        return context