from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime
from .models import Post, Category
from django.conf import settings


@shared_task
def send_mail(preview, pk, title, subscribers):
    html_context = render_to_string(
        'new_post_email.html',
        {'text': preview, 'link': f'http://127.0.0.1/news/{pk}'})
    msg = EmailMultiAlternatives(
        subject=title, body='', from_email='seirana.ramazanova@yandex.ru', to=subscribers)
    msg.attach_alternative(html_context, 'text/html')
    msg.send()



@shared_task
def my_job():
    today = datetime.datetime.now()
    last_week = today-datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string('daily_post.html', {'link': settings.SITE_URL, 'posts': posts})
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()