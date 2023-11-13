from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('films/', FilmsView.as_view(), name='films'),
    path('addrating/', AddRating.as_view(), name='add_rating'),
    path('account/<str:username>', Account.as_view(), name='account'),
    path('search/', Search.as_view(), name='search'),
    path('films/<slug:cat_slug>/', FilmCategoryView.as_view(), name='filmcategory'),
    path('films/year', FilmYearView.as_view(), name='filmyear'),
    path('film/<int:pk>/', FilmView.as_view(), name='film'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('persons/<int:pk>', PersonView.as_view(), name='persons'),
    path('registration/', Registration.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
]