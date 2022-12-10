from django.shortcuts import render  # обычный render - нам больше не нужен
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from store.models import Book
from store.permissions import MyIsOwnerOrStaffOrReadOnly
from store.serializers import BookSerializer


# ModelViewSet - родительский класс
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()  # объекты нашей модели
    serializer_class = BookSerializer  # наш сериализатор
    # только авторизованные пользователи и владельцы могут изменять записи - а смотреть могут все
    permission_classes = [MyIsOwnerOrStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # django-filter
    # для фильтра в url  - ?price=1000
    filter_fields = ['price']  # django-filter - возможность фильтровать по price (цене)
    # для поиска
    search_fields = ['name', 'author_name']
    # для сортировки
    ordering_fields = ['price', 'author_name']

    # дополняем поведение при создании книги
    def perform_create(self, serializer):
        # В модель Book - в поле owner - присвоим инфу о пользователе
        serializer.validated_data['owner'] = self.request.user
        serializer.save()  # сохраняем


def my_auth(request):
    return render(request, 'oauth.html')


