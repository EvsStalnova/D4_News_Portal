from django.db import models  # Импортируем модуль models из Django для определения моделей базы данных
from django.contrib.auth.models import User  # Импортируем модель User из модуля auth Django
from django.db.models import Sum  # Импортируем функцию Sum из модуля models Django для агрегации суммы значений
from django.urls import reverse


class Author(models.Model):  # Определяем модель Author, наследуясь от models.Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Поле user типа OneToOneField, связанное с моделью User
    rating = models.IntegerField(default=0)  # Поле rating типа IntegerField с значением по умолчанию 0

    def update_rating(self):  # Определяем метод update_rating
        post_rating = self.post_set.aggregate(post_rating=Sum('rating'))['post_rating'] or 0  # Сумма рейтингов всех постов автора
        comment_rating = self.user.comment_set.aggregate(comment_rating=Sum('rating'))['comment_rating'] or 0  # Сумма рейтингов всех комментариев пользователя

        pRat = 0  # Инициализируем переменную pRat со значением 0
        pRat += post_rating  # Увеличиваем значение переменной pRat на значение post_rating

        cRat = 0  # Инициализируем переменную cRat со значением 0
        cRat += comment_rating  # Увеличиваем значение переменной cRat на значение comment_rating

        self.rating = pRat * 3 + cRat  # Расчет обновленного рейтинга автора
        self.save()  # Сохранение изменений

    def __str__(self):
        return self.user.username


class Category(models.Model):  # Определяем модель Category, наследуясь от models.Model
    name = models.CharField(max_length=255, unique=True)  # Поле name типа CharField с максимальной длиной 255 символов и уникальным значением

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):  # Определяем модель Post, наследуясь от models.Model
    news = 'news'
    post = 'post'

    POST_TYPES = [  # Кортеж POST_TYPES с определенными вариантами выбора
        (news, 'Новость'),
        (post, 'Статья')
    ]
    author = models.ForeignKey(Author,on_delete=models.CASCADE)  # Поле author типа ForeignKey, связанное с моделью Author
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default=news)  # Поле post_type типа CharField с максимальной длиной 10 символов и выбором из POST_TYPES
    created_at = models.DateTimeField(auto_now_add=True)  # Поле created_at типа DateTimeField с автоматическим добавлением текущей даты и времени при создании
    categories = models.ManyToManyField(Category, through='PostCategory')  # Связь "многие ко многим" с моделью Category через модель PostCategory
    title = models.CharField(max_length=255)  # Поле title типа CharField с максимальной длиной 255 символов
    content = models.TextField()  # Поле content типа TextField
    rating = models.IntegerField(default=0)  # Поле rating типа IntegerField с значением по умолчанию 0

    def like(self):  # Определяем метод like
        self.rating += 1  # Увеличиваем значение рейтинга на 1
        self.save()  # Сохранение изменений

    def dislike(self):  # Определяем метод dislike
        self.rating -= 1  # Уменьшаем значение рейтинга на 1
        self.save()  # Сохранение изменений

    def preview(self):  # Определяем метод preview
        return f'{self.content[:124]} ...'    # Возвращаем превью содержимого поста с добавлением рейтинга

    def __str__(self):
        return f'{self.title}: {self.content}'

    def get_absolute_url(self):
        return reverse('post:post_detail', args=[str(self.id)])


class PostCategory(models.Model):  # Определяем модель PostCategory, наследуясь от models.Model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Поле post типа ForeignKey, связанное с моделью Post
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Поле category типа ForeignKey, связанное с моделью Category


class Comment(models.Model):  # Определяем модель Comment, наследуясь от models.Model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Поле post типа ForeignKey, связанное с моделью Post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Поле user типа ForeignKey, связанное с моделью User
    text = models.TextField()  # Поле text типа TextField
    created_at = models.DateTimeField(auto_now_add=True)  # Поле created_at типа DateTimeField с автоматическим добавлением текущей даты и времени при создании
    rating = models.IntegerField(default=0)  # Поле rating типа IntegerField с значением по умолчанию 0

    def like(self):  # Определяем метод like
        self.rating += 1  # Увеличиваем значение рейтинга на 1
        self.save()  # Сохранение изменений

    def dislike(self):  # Определяем метод dislike
        self.rating -= 1  # Уменьшаем значение рейтинга на 1
        self.save()  # Сохранение изменений

    def __str__(self):
        return self.text