from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscription, PostCategory
from django.urls import reverse_lazy
from .forms import PostForm
from .filters import NewsFilter
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef



@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user, category=category).delete()

    categories_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(
        Subscription.objects.filter(user=request.user, category=OuterRef('pk')))).order_by('name')

    return render(request, 'subscriptions.html', {'categories': categories_with_subscriptions},)


class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2


class Search(NewsList):
    template_name = 'search.html'
    context_object_name = 'news_search'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['something'] = 'some'
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news_create'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.categoryType = 'AR'
        elif self.request.path == '/news/create/':
            post.categoryType = 'NW'
        post.save()
        return super().form_valid(form)


    success_url = reverse_lazy('news_list')

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news_update'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news_delete'
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')