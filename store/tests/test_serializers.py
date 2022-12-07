from django.test import TestCase
from django.urls import reverse
from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        # вводные данные
        book_1 = Book.objects.create(name='Test book 1', price=25)
        book_2 = Book.objects.create(name='Test book 2', price=50)
        # проверяемые данные
        data = BookSerializer([book_1, book_2], many=True).data

        # ожидаемые данные
        expected_data =[
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00'
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '50.00'
            },
        ]

        # само тестирование
        # (ожидаемые данные, данные из сериализатора)
        self.assertEqual(expected_data, data)











        BookSerializer

        url = reverse('book-list')

        # self.client - например клиент/браузер - который делает запрос нашему серверу
        response = self.client.get(url)