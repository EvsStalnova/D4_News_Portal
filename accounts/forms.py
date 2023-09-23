from allauth.account.forms import SignupForm
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class CustomSignUpForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        subject = 'Добро пожаловать на наш новостной портал!'
        text = f'{user.username}, Вы успешно зарегистрировались на нашем новостном портале!'
        html = (
            f'<b>{user.username}</b>, Вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/post">нашем новостном портале!</a>'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        return user


