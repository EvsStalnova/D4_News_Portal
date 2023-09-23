from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import *
from .tasks import *


@receiver(m2m_changed, sender=PostCategory)
def post_created(instance, sender, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_send.delay(instance.id)




