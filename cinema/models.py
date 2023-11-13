from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=400, verbose_name='Описание')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('filmcategory', kwargs={'cat_slug': self.slug})

class Person(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    age = models.PositiveIntegerField(verbose_name='Возраст', default=0)
    description = models.TextField(max_length=600, verbose_name='Описание')
    photo = models.ImageField(verbose_name='Фотография', upload_to='people/')

    class Meta:
        verbose_name = 'Деятель'
        verbose_name_plural = 'Деятели'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('persons', kwargs={'pk': self.id})


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=300, verbose_name='Описание')
    url = models.SlugField(verbose_name='URL', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slogan = models.CharField(max_length=150, verbose_name='Слоган')
    poster = models.ImageField(verbose_name='Постер', upload_to='movies/')
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')
    description = models.TextField(max_length=600, verbose_name='Описание')
    year = models.SmallIntegerField(verbose_name='Год выпуска', default='2000')
    date = models.DateField(verbose_name='Дата выхода в прокат')
    country = models.CharField(max_length=100, verbose_name='Страна')
    directors = models.ManyToManyField(Person, verbose_name='Режисеры', related_name='film_directors')
    actors = models.ManyToManyField(Person, verbose_name='Актеры', related_name='film_actors')
    budget = models.TextField(max_length=100, verbose_name='Бюджет')
    fee = models.TextField(max_length=100, verbose_name='Сборы в мире')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(verbose_name='URL', unique=True)
    draft = models.BooleanField(verbose_name='Черновик', default=False)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('film', kwargs={'pk': self.id})


class FilmPics(models.Model):
    image = models.ImageField(verbose_name='Кадр из фильма', upload_to='posters/')
    film = models.ForeignKey(Film, verbose_name='Фильм', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Кадр'
        verbose_name_plural = 'Кадры'

    def __str__(self):
        return f"Кадры из фильма '{self.film}'"


class Stars(models.Model):
    count = models.PositiveIntegerField(verbose_name='Количество', default=1)

    class Meta:
        verbose_name = 'Звезда'
        verbose_name_plural = 'Звезды'

    def __str__(self):
        return str(self.count)


class Rating(models.Model):
    ip = models.CharField(verbose_name='IP адрес', max_length=20)
    stars = models.ForeignKey(Stars, on_delete=models.CASCADE, verbose_name='Звезды')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return str(self.stars)


class Reviews(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(max_length=100, verbose_name='Email')
    review = models.TextField(max_length=2000, verbose_name='Комментарий')
    date = models.DateTimeField(auto_now_add=True)
    film = models.ForeignKey(Film, verbose_name='Фильм', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв на фильм {self.film} от пользователя {self.name}"






