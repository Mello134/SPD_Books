from rest_framework.serializers import ModelSerializer
from store.models import Book


# ModelSerializer - родительский класс
class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # все поля
