from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


# Создавайте свои модели здесь.
class Author(models.Model):
    """
    Метод update_rating() вычисляет суммарный рейтинг каждой статьи автора,
    умножает его на 3, а затем складывает с суммарным рейтингом всех комментариев автора
    и комментариев к статьям автора.
    Результат сохраняется в поле rating объекта Author
    """

    autUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAut = models.SmallIntegerField(default=0)

    def update_rating(self):
        # Вычисление суммарного рейтинга статей автора
        post_sum = self.post_set.aggregate(postRating=Sum('rating'))  # Сбор всех данных определённого поля автора
        temp_sum_p = 0
        temp_sum_p += post_sum.get('postRating')
        # Вычисление суммарного рейтинга комментариев автора
        comment_sum = self.autUser.comment_set.aggregate(commentRating=Sum('rating'))
        temp_sum_c = 0
        temp_sum_c += comment_sum.get('commentRating')

        self.ratingAut = temp_sum_p * 3 + temp_sum_c
        self.save()

    # для удобного отображения на странице администратора
    def __str__(self):
        return self.autUser.username


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    # для отображения имён вместо объектов
    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Метод preview() возвращает начало статьи длиной 124 символа с многоточием в конце
    Методы like() и dislike() увеличивают/уменьшают рейтинг на единицу.
    """
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGOY_CHOICES = (
        ('AR', 'Статья'),
        ('NW', 'Новость'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Поле Автор
    type = models.CharField(max_length=2, choices=CATEGOY_CHOICES, default=ARTICLE)  # Поле выбора новость / статья
    creationDate = models.DateTimeField(auto_now_add=True)  # Авто добавление даты создания
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:123]} ...'

    # для удобного отображения на странице администратора
    def __str__(self):
        return self.title

    # какую страницу нужно открыть после создания
    def get_absolute_url(self):
        return reverse('Start', args=[str(self.id)])


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    # для удобного отображения на странице администратора
    def __str__(self):
        return self.postThrough


class Comment(models.Model):
    """
    Методы like() и dislike() увеличивают/уменьшают рейтинг на единицу.
    """
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # для удобного отображения на странице администратора
    def __str__(self):
        return self.text