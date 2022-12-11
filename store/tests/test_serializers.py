from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase
from django.urls import reverse
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


# тест сериализатора
class BookSerializerTestCase(TestCase):
    def test_ok(self):
        # вводные данные
        user1 = User.objects.create(username='username1')
        user2 = User.objects.create(username='username2')
        user3 = User.objects.create(username='username3')
        book_1 = Book.objects.create(name='Test book 1', price=25,
                                     author_name='Author 1')
        book_2 = Book.objects.create(name='Test book 2', price=50,
                                     author_name='Author 2')

        # все пользователи поставили лайк на первую книгу, и поставили рейтинг 5
        UserBookRelation.objects.create(user=user1, book=book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True,
                                        rate=5)

        # 2 пользователя поставили лайк на вторую книгу, и поставили разный рейтинг
        UserBookRelation.objects.create(user=user1, book=book_2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=False)
        UserBookRelation.objects.create(user=user3, book=book_2, like=True,
                                        rate=4)

        # проверяемые данные
        books = Book.objects.all().annotate(
            # annotated_likes(Считаем лайки(Case(когда будет работать(Если стоит лайк, возвращаем 1)
            # userbookrelation__like - через книгу пробираемся к relation, через relation к лайку, then=1)
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            # аннотация рейтинга
            # Avg - average - среднее значение
            rating=Avg('userbookrelation__rate'),
        ).order_by('id')
        data = BookSerializer(books, many=True).data

        # ожидаемые данные
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1',
                'likes_count': 3,  # будем ожидать 3 лайка
                'annotated_likes': 3,  # будем ожидать 3 лайка
                'rating': '5.00',
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '50.00',
                'author_name': 'Author 2',
                'likes_count': 2,  # будем ожидать 2 лайка
                'annotated_likes': 2,  # будем ожидать 2 лайка
                'rating': '3.50',
            },
        ]

        # само тестирование
        # (ожидаемые данные, данные из сериализатора)
        self.assertEqual(expected_data, data)


