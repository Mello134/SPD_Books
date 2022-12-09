from django.shortcuts import render  # обычный render - нам больше не нужен
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from store.models import Book
from store.serializers import BookSerializer


# ModelViewSet - родительский класс
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()  # объекты нашей модели
    serializer_class = BookSerializer  # наш сериализатор

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # django-filter
    # для фильтра в url  - ?price=1000
    filter_fields = ['price']  # django-filter - возможность фильтровать по price (цене)
    # для поиска
    search_fields = ['name', 'author_name']
    # для сортировки
    ordering_fields = ['price', 'author_name']


