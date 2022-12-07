from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


# проверка API  - см urls.py router.register(r'book', BookViewSet)
class BooksApiTestCase(APITestCase):
    def test_get(self):
        # вводные данные
        book_1 = Book.objects.create(name='Test book 1', price=25)
        book_2 = Book.objects.create(name='Test book 2', price=50)

        # book-list - получение всего списка router.register(r'book', BookViewSet)
        # book-detail - если бы необходимо было бы конкретную книгу
        url = reverse('book-list')

        # self.client - например клиент/браузер - который делает запрос нашему серверу
        response = self.client.get(url)

        # Ожидаем страницу статус=200, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # сравниваем то что вводные данные сходятся с выходными
        serializer_data = BookSerializer([book_1,book_2], many=True).data
        # serializer_data - входные данные, response.data - выходные данные
        # Мы ожидаем что должно быть serializer_data, и проверяем равен ли ей response.data
        self.assertEqual(serializer_data, response.data)


