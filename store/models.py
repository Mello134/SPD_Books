from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    name = models.CharField(verbose_name='Название книги', max_length=255)
    # DecimalField - почти float, но необходимо указать сколько значений будет после запятой
    # max_digits=7 - максимальное количество цифр в числе (вместе с дробной частью)
    # decimal_places=2 - два числа после запятой
    price = models.DecimalField(verbose_name='Цена книги', max_digits=7, decimal_places=2)
    author_name = models.CharField(verbose_name='Автор книги', max_length=255)
    # owner - владелец -один
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, related_name='my_books', verbose_name='Владелец')
    # читатель - много читателей
    readers = models.ManyToManyField(User, through='UserBookRelation',
                                     related_name='read_books', verbose_name='Читатели')
    # рейтинг 3.68
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f'Id {self.pk}: {self.name}'


# Пользователь - книга
class UserBookRelation(models.Model):
    # оценка рейтинга - варианты выбора
    # 1 - то что хранится в базе, 2 - то что будет отображаться *на фронте, в админке)
    RATE_CHOICES = (
        (1, 'Очень плохо'),
        (2, 'Плохо'),
        (3, 'Средне'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    )

    # связь с пользователем
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    # связь с книгой
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Кинга')
    # учёт лайков (True - +1, False = нет дайка)
    like = models.BooleanField(default=False, verbose_name='Лайк')
    # добавлена в закладки (избранное)
    is_bookmarks = models.BooleanField(default=False, verbose_name='Закладка')
    # рейтинг (оценка пользователя для книги)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True, verbose_name='Оценка')

    class Meta:
        verbose_name = 'Отношение пользователя к книге'
        verbose_name_plural = 'Отношения пользователей к книгам'

    def __str__(self):
        return f'Пользователь:{self.user.username} - Книга:{self.book.name}, Рейтинг:{self.rate}'

    def save(self, *args, **kwargs):
        # локальный импорт
        from store.logic import set_rating

        creating = not self.pk
        old_rating = self.rate

        # через super - мы обращаемся к родительскому элементу Models
        # чтобы не сломать стандартные поля
        # делаем super -чтобы наш def save тоже вызвался
        super().save(*args, **kwargs)

        new_rating = self.rate

        # если old - не как - new, будем делать пересчёт
        if old_rating != new_rating or creating:
            set_rating(self.book)



