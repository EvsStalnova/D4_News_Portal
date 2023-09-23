from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from datetime import datetime
from .filters import PostFilter
from .models import *
from .forms import PostForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/post.html'
    context_object_name = 'post'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('post.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('post.delete_post',)
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('post.update_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_update.html'
    success_url = reverse_lazy('post_list')


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
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'flatpages/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )






