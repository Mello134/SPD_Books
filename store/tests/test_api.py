import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


# проверка API  - см urls.py router.register(r'book', BookViewSet)
class BooksApiTestCase(APITestCase):
    # метод будет запускаться перед каждым тестом (методами test_get)
    def setUp(self):
        self.user = User.objects.create(username='test_username')

        # вводные данные
        self.book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Автор 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=50, author_name='Автор 2')
        self.book_3 = Book.objects.create(name='Test book 3 Автор 1', price=75, author_name='Автор 1')

    def test_get(self):
        # book-list - получение всего списка router.register(r'book', BookViewSet)
        # book-detail - если бы необходимо было бы конкретную книгу
        url = reverse('book-list')

        # self.client - например клиент/браузер - который делает запрос нашему серверу
        response = self.client.get(url)

        # Ожидаем страницу статус=200, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # сравниваем то что вводные данные сходятся с выходными
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        # serializer_data - входные данные, response.data - выходные данные
        # Мы ожидаем что должно быть serializer_data, и проверяем равен ли ей response.data
        self.assertEqual(serializer_data, response.data)

    def test_get(self):
        # book-list - получение всего списка router.register(r'book', BookViewSet)
        # book-detail - если бы необходимо было бы конкретную книгу
        url = reverse('book-list')

        # self.client - например клиент/браузер - который делает запрос нашему серверу
        response = self.client.get(url)

        # Ожидаем страницу статус=200, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # сравниваем то что вводные данные сходятся с выходными
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        # serializer_data - входные данные, response.data - выходные данные
        # Мы ожидаем что должно быть serializer_data, и проверяем равен ли ей response.data
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        # количество книг до добавления - ожидаем 3
        self.assertEqual(3, Book.objects.all().count())

        # book-list - получение всего списка router.register(r'book', BookViewSet)
        # book-detail - если бы необходимо было бы конкретную книгу
        url = reverse('book-list')

        # условия поиска
        response = self.client.get(url, data={'search': 'Автор 1'})
        # Ожидаем страницу статус=200, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer_data = BookSerializer([self.book_1,
                                          self.book_3], many=True).data
        # Мы ожидаем что должно быть serializer_data, и проверяем равен ли ей response.data
        self.assertEqual(serializer_data, response.data)

    def test_post_create(self):
        # количество книг до добавления - ожидаем 3
        self.assertEqual(3, Book.objects.all().count())

        # book-list - получение всего списка router.register(r'book', BookViewSet)
        # book-detail - если бы необходимо было бы конкретную книгу
        url = reverse('book-list')

        # Данные которые попытаемся записать
        data = {"name": "Пайтон 3",
                "price": "150.00",
                "author_name": "Марк Шумерфилд"
                }

        # преобразуем наши данные в формат json
        json_data = json.dumps(data)

        # сделаем авторизацию, так как сейчас мы ограничели доступ
        self.client.force_login(self.user)

        # проверяемые данные, post запрос
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')

        # Ожидаем страницу статус=201, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # сравниваем количество книг, ожидаем 4
        self.assertEqual(4, Book.objects.all().count())

    def test_put_update(self):
        # book-list - получение всего списка router.register(r'book', BookViewSet)
        # book-detail - если бы необходимо было бы конкретную книгу
        # нам обязательно необходимо получить id - чтобы понять какую книгу менять, получаем в args
        url = reverse('book-detail', args=(self.book_1.id,))

        # Данные которые попытаемся записать / поменять цену
        data = {"name": self.book_1.name,
                "price": 1500,
                "author_name": self.book_1.author_name
                }

        # преобразуем наши данные в формат json
        json_data = json.dumps(data)

        # сделаем авторизацию, так как сейчас мы ограничели доступ
        self.client.force_login(self.user)

        # проверяемые данные, post запрос
        response = self.client.put(url, data=json_data,
                                    content_type='application/json')

        # Ожидаем страницу статус=200, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # перезаписываем данные изменённой книги 1
        self.book_1.refresh_from_db()

        # проверяем изменилась ли цена
        self.assertEqual(1500, self.book_1.price)

