import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


# проверка API  - см urls.py router.register(r'book', BookViewSet)
class BooksApiTestCase(APITestCase):
    # метод будет запускаться перед каждым тестом (методами test_get)
    def setUp(self):
        self.user = User.objects.create(username='test_username')

        # вводные данные
        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Автор 1', owner=self.user)
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

        # сделаем авторизацию, так как сейчас мы ограничили доступ
        self.client.force_login(self.user)

        # проверяемые данные, post запрос
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')

        # Ожидаем страницу статус=201, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # сравниваем количество книг, ожидаем 4
        self.assertEqual(4, Book.objects.all().count())

        # сравниваем поле owner (инфа владельца)
        # сравниваем текущий пользователь = запись о владельце модели Book
        self.assertEqual(self.user, Book.objects.last().owner)

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

    # сценарий когда не владелец книги пытается изменить данные книги
    def test_put_update_not_owner(self):
        # это будет не владелец книги
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {"name": self.book_1.name,
                "price": 1500,
                "author_name": self.book_1.author_name
                }
        json_data = json.dumps(data)
        # авторизация не владельца книги
        self.client.force_login(self.user2)
        # проверяемые данные, post запрос
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        # Ожидаем страницу статус=403 - запрет доступа, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        # перезаписываем данные изменённой книги 1
        self.book_1.refresh_from_db()
        # проверяем изменилась ли цена - ожидаем что изменения не произойдёт
        self.assertEqual(25, self.book_1.price)

    # сценарий когда не владелец книги пытается изменить данные книги
    def test_put_update_not_owner_but_staff(self):
        # это будет не владелец книги, но админ
        self.user2 = User.objects.create(username='test_username2',
                                         is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {"name": self.book_1.name,
                "price": 1500,
                "author_name": self.book_1.author_name
                }
        json_data = json.dumps(data)
        # авторизация не владельца книги
        self.client.force_login(self.user2)
        # проверяемые данные, post запрос
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        # Ожидаем страницу статус=200 - всё ок, сравниваем с ответным кодом
        # 200 - потому что изменяет админ и должно получится
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # перезаписываем данные изменённой книги 1
        self.book_1.refresh_from_db()
        # проверяем изменилась ли цена - ожидаем что изменилось
        self.assertEqual(1500, self.book_1.price)


class BooksRelationTestCase(APITestCase):
    # метод будет запускаться перед каждым тестом (методами test_get)
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        # вводные данные
        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Автор 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=50, author_name='Автор 2')

    def test_patch_like(self):
        # reverse - смотри в 404 странице в браузере, по name=''
        # там же смотри что нам нужно id книги
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        # по дефолту лайк = False
        data = {"like": True,

                }
        json_data = json.dumps(data)

        # авторизуем пользователя 1
        self.client.force_login(self.user)
        # self.client - например клиент/браузер - который делает запрос нашему серверу
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        # Ожидаем страницу статус=200, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # отношение каким пользователем какая книга пролайкана
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)

        # ожидаем что лайк будет True
        self.assertEqual(True, relation.like)
        # self.assertTrue(relation.like)

    def test_patch_is_bookmarks(self):
        # reverse - смотри в 404 странице в браузере, по name=''
        # там же смотри что нам нужно id книги
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        # по дефолту закладка = False
        data = {
            "is_bookmarks": True,
                }
        json_data = json.dumps(data)

        # авторизуем пользователя 1
        self.client.force_login(self.user)
        # self.client - например клиент/браузер - который делает запрос нашему серверу
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        # Ожидаем страницу статус=200, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # отношение каким пользователем какая книга добавлена в закладки
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)

        # ожидаем что добавится в закладки
        self.assertEqual(True, relation.is_bookmarks)
        # self.assertTrue(relation.is_bookmarks)

    def test_patch_rate(self):
        # reverse - смотри в 404 странице в браузере, по name=''
        # там же смотри что нам нужно id книги
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        # по дефолту рейтинг = null
        data = {
            "rate": 5,
                }
        json_data = json.dumps(data)

        # авторизуем пользователя 1
        self.client.force_login(self.user)
        # self.client - например клиент/браузер - который делает запрос нашему серверу
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        # Ожидаем страницу статус=200, сравниваем с ответным кодом
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # отношение каким пользователем какой книге поставит рейтинг
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)

        # ожидаем что рейтинг будет 5
        self.assertEqual(5, relation.rate)

    def test_patch_rate_wrong(self):
        # reverse - смотри в 404 странице в браузере, по name=''
        # там же смотри что нам нужно id книги
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        # по дефолту рейтинг = null
        # 6 - может быть по условию модели
        data = {
            "rate": 6,
                }
        json_data = json.dumps(data)

        # авторизуем пользователя 1
        self.client.force_login(self.user)
        # self.client - например клиент/браузер - который делает запрос нашему серверу
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')

        # Ожидаем страницу статус=200, сравниваем с ответным кодом
        # третий аргумент - если что-то не сошлось (какой сделать принт)
        # то есть 3-й аргумент скажет, почему не вышло получить 200
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)

        # отношение каким пользователем какой книге поставит рейтинг
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)

        # ожидаем что рейтинг будет 5 (то есть он не изменится с прошлого теста, так как 6 не может быть)
        self.assertEqual(5, relation.rate)


