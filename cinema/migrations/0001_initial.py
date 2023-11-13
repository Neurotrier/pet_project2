# Generated by Django 4.2.6 on 2023-10-27 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(max_length=400, verbose_name='Описание')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slogan', models.CharField(max_length=150, verbose_name='Слоган')),
                ('poster', models.ImageField(upload_to='movies/', verbose_name='Постер')),
                ('description', models.TextField(max_length=600, verbose_name='Описание')),
                ('year', models.SmallIntegerField(default='2000', verbose_name='Год выпуска')),
                ('date', models.DateField(verbose_name='Дата выхода в прокат')),
                ('country', models.CharField(max_length=100, verbose_name='Страна')),
                ('budget', models.TextField(max_length=100, verbose_name='Бюджет')),
                ('fee', models.TextField(max_length=100, verbose_name='Сборы в мире')),
                ('url', models.SlugField(unique=True, verbose_name='URL')),
                ('draft', models.BooleanField(default=False, verbose_name='Черновик')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(max_length=300, verbose_name='Описание')),
                ('url', models.SlugField(unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('age', models.PositiveIntegerField(default=0, verbose_name='Возраст')),
                ('description', models.TextField(max_length=600, verbose_name='Описание')),
                ('photo', models.ImageField(upload_to='people/', verbose_name='Фотография')),
            ],
            options={
                'verbose_name': 'Деятель',
                'verbose_name_plural': 'Деятели',
            },
        ),
        migrations.CreateModel(
            name='Stars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1, verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Звезда',
                'verbose_name_plural': 'Звезды',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('review', models.TextField(max_length=2000, verbose_name='Комментарий')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.film', verbose_name='Фильм')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20, verbose_name='IP адрес')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.film')),
                ('stars', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.stars', verbose_name='Звезды')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='FilmPics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='posters/', verbose_name='Кадр из фильма')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.film', verbose_name='Фильм')),
            ],
            options={
                'verbose_name': 'Кадр',
                'verbose_name_plural': 'Кадры',
            },
        ),
        migrations.AddField(
            model_name='film',
            name='actors',
            field=models.ManyToManyField(related_name='film_actors', to='cinema.person', verbose_name='Актеры'),
        ),
        migrations.AddField(
            model_name='film',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinema.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='film',
            name='directors',
            field=models.ManyToManyField(related_name='film_directors', to='cinema.person', verbose_name='Режисеры'),
        ),
        migrations.AddField(
            model_name='film',
            name='genre',
            field=models.ManyToManyField(to='cinema.genre', verbose_name='Жанры'),
        ),
    ]
