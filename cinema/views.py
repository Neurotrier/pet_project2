from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, viewsets
from .models import *
from .forms import *
from .serializers import *

"""Этот модуль обрабатывает обычный зарпосы Django"""


def home_page(request):
    return HttpResponse('Привет, мир!')


class Account(ListView):
    template_name = 'cinema/account.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Reviews.objects.filter(name=self.request.user.username)




class FilmsView(ListView):
    model = Film
    queryset = Film.objects.all()
    template_name = 'cinema/films.html'
    context_object_name = 'films'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['years'] = set(i['year'] for i in Film.objects.all().values('year'))
        return context


class FilmCategoryView(ListView):
    model = Film
    template_name = 'cinema/films.html'
    context_object_name = 'films'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cat_selected'] = Category.objects.get(slug=self.kwargs['cat_slug']).pk
        return context

    def get_queryset(self):
        return Film.objects.filter(category__slug = self.kwargs['cat_slug'])


class FilmYearView(ListView):
    model = Film
    template_name = 'cinema/films.html'
    context_object_name = 'films'

    def get_queryset(self):
        print(Film.objects.filter(year__in=self.request.GET.getlist('year')))
        return Film.objects.filter(year__in=self.request.GET.getlist('year'))

class PersonView(DetailView):
    model = Person
    template_name = 'cinema/persons.html'
    context_object_name = 'person'



class FilmView(DetailView):
    model = Film
    template_name = 'cinema/film.html'
    context_object_name = 'film'
    slug_url_kwarg = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['range'] = range(1,6)
        c = Rating.objects.filter(film__id=self.kwargs['pk'])
        a = c.aggregate(Avg('stars'))
        context['c'] = a['stars__avg']
        return context


class AddReview(LoginRequiredMixin, View):
    login_url = 'login'
    def post(self, request, pk):
        if request.POST.get('review'):
            Reviews.objects.create(
                name=request.user.username,
                email=request.user.email,
                review=request.POST.get('review'),
                film_id=pk
            )
            return redirect('film', int(pk))
        # form = ReviewForm(request.POST)
        # film = Film.objects.get(id=pk)
        # if form.is_valid():
        #     print(form.cleaned_data)
        #     form = form.save(commit=False)
        #     form.film = film
        #     form.save()
        # return redirect(film.get_absolute_url())



class Registration(CreateView):
    form_class = RegisterForm
    template_name = 'cinema/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class Login(LoginView):
    form_class = LoginForm
    template_name = 'cinema/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('films')

class AddRating(View):
    def get_client_id(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        print(request.POST)
        print(self.get_client_id(request))
        if request.POST.get('stars'):
            Rating.objects.update_or_create(
                    ip=self.get_client_id(request),
                    film_id=int(request.POST.get('film')),
                    defaults={"stars_id": int(request.POST.get('stars'))}
            )
        return redirect('film', int(request.POST.get('film')))

class Search(ListView):
    model = Film
    template_name = 'cinema/search.html'
    context_object_name = 'films'

    def get_queryset(self):
        return Film.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_years(self):
        return Film.objects.filter(title__icontains=self.request.GET.get('q')).values('year')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        context['years'] = set(i['year'] for i in self.get_years())
        context['q'] = self.request.GET.get('q')
        return context


"""Этот модуль работает с апи - DRF"""
class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

