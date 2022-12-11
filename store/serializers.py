from rest_framework.serializers import ModelSerializer
from store.models import Book, UserBookRelation


# ModelSerializer - родительский класс
class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # все поля


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'is_bookmarks', 'rate')  # поля
        # 'user' - не будем добавлять, так как его можно взять из request.user.username


