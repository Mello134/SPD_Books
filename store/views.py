from django.db.models import Count, Case, When, Avg
from django.shortcuts import render  # обычный render - нам больше не нужен
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from store.models import Book, UserBookRelation
from store.permissions import MyIsOwnerOrStaffOrReadOnly
from store.serializers import BookSerializer, UserBookRelationSerializer


# ModelViewSet - родительский класс
class BookViewSet(ModelViewSet):
    # объекты
    queryset = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        ).select_related('owner').prefetch_related('readers').order_by('id')

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


class UserBooksRelationView(UpdateModelMixin,
                            GenericViewSet):
    # права
    permission_classes = [IsAuthenticated]  # только авторизованный
    # данные
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'  # id книги

    # переопределим метод
    def get_object(self):
        # get_or_create (получить отношение если есть,
        #                создать его если нету)
        # obj - это объект
        # _ - created (создан или найден)
        # book_id - пришёл через lookup_field в виде словаря
        # Мы получаем доступ к модели UserBookRelation - через переданный параметр книги, и пользователя из request
        # если такой связи нет мы создадим её - get_or_create
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        return obj


def my_auth(request):
    return render(request, 'oauth.html')


