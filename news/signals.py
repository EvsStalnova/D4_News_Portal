from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.conf import settings
from .models import *


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        emails = User.objects.filter(
            subscriptions__category=instance.category
        ).values_list('email', flat=True)

        subject = f'Новая публикация в категории {instance.category}'

        text_content = (
            f'Публикация: {instance.title}\n'
            f'{instance.text}\n\n'
            f'Ссылка на публикацию: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Публикация: {instance.title}<br>'
            f'Цена: {instance.text}<br><br>'
            f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
            f'Ссылка на публикацию</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

