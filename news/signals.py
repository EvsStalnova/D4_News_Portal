from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .tasks import send_mail
from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()
        subscribers = [s.email for s in subscribers]
        send_mail(instance.preview(), instance.pk, instance.title, subscribers)

        emails = User.objects.filter(subscriptions__category=instance.category).values_list('email', flat=True)
        subject = f'Новый пост в категории {instance.category}'
        text_content = (
            f'Пост {instance.title}\n'
            f'{instance.text}\n\n'
            f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Пост {instance.title}<br>'
            f'{instance.text}<br><br>'
            f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
            f'Ссылка на пост</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
signals.post_save.connect

