from django.shortcuts import render  # обычный render - нам больше не нужен
from rest_framework.viewsets import ModelViewSet

from store.models import Book
from store.serializers import BookSerializer


# ModelViewSet - родительский класс
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()  # объекты нашей модели
    serializer_class = BookSerializer  # наш сериализатор

