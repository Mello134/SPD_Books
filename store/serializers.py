from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from store.models import Book, UserBookRelation


class BookReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


# ModelSerializer - родительский класс
class BookSerializer(ModelSerializer):
    # поле количество лайков через annotated
    annotated_likes = serializers.IntegerField(read_only=True)
    # рейтинг по типу 1.77, 4,50, 3,93
    rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    # имя владельца
    # read_only=True - поле только для чтение
    owner_name = serializers.CharField(source='owner.username', default='',
                                       read_only=True)
    # читатели
    readers = BookReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name',
                  'annotated_likes', 'rating', 'owner_name',
                  'readers', )  # поля


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'is_bookmarks', 'rate')  # поля
        # 'user' - не будем добавлять, так как его можно взять из request.user.username

