from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    name = models.CharField(verbose_name='Название книги', max_length=255)
    # DecimalField - почти float, но необходимо указать сколько значений будет после запятой
    # max_digits=7 - максимальное количество цифр в числе (вместе с дробной частью)
    # decimal_places=2 - два числа после запятой
    price = models.DecimalField(verbose_name='Цена книги', max_digits=7, decimal_places=2)
    author_name = models.CharField(verbose_name='Автор книги', max_length=255)
    # owner - владелец
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True)

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f'Id {self.id}: {self.name}'


