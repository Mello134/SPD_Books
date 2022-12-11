from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from store.models import Book, UserBookRelation


# ModelSerializer - родительский класс
class BookSerializer(ModelSerializer):
    # поле количество лайков
    likes_count = serializers.SerializerMethodField()
    # поле количество лайков через annotated
    annotated_likes = serializers.IntegerField(read_only=True)
    # рейтинг по типу 1.77, 4,50, 3,93
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'likes_count', 'annotated_likes', 'rating')  # поля

    # считаем количество лайков - ручным способом
    # instance - та самая книга, которую в данный момент сериализуем
    def get_likes_count(self, instance):
        # считаем объекты - выбранная книга, у которой есть отношение like=True
        return UserBookRelation.objects.filter(book=instance, like=True).count()





class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'is_bookmarks', 'rate')  # поля
        # 'user' - не будем добавлять, так как его можно взять из request.user.username


