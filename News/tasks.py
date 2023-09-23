from celery import shared_task
import datetime
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from .signals import *
from .models import *


@shared_task
def new_post_send(post_id):
    post = Post.objects.get(pk=post_id)
    emails = User.objects.filter(
        subscriptions__category=post.postCategory.all()[0]
    ).values_list('email', flat=True)
    subject = f'Новая публикация в категории {post.postCategory.all()[0].name}'
    text_content = (
        f'Публикация на тему: {post.title}\n'
        f'Текст: {post.text[0:124]}' + '...\n\n'
        f'Полностью публикацию Вы можете прочитать на нашем сайте: http://127.0.0.1:8000{post.get_absolute_url()}'
    )
    html_content = (
        f'Публикация: {post.title}<br>'
        f'Текст: {post.text[0:124]}' + '...<br><br>'
        f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
        f'Полностью публикацию Вы можете прочитать на нашем сайте</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_send_email_task():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    post = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(post.values_list('postCategory__id', flat=True))
    subscribers = set(Subscription.objects.filter(category__in=categories).values_list('user__email', flat=True))
    print(f'{subscribers = }')
    html_content = render_to_string(
        'flatpages/weekly_postletter.html',
        {
            'link': f'{settings.SITE_URL}',
            'post': post,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Это наша еженедельная рассылка',
        body='',
        from_email='stanislaskropotin@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()