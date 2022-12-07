from django.db import models


class Book(models.Model):
    name = models.CharField(verbose_name='Название книги', max_length=255)
    # DecimalField - почти float, но необходимо указать сколько значений будет после запятой
    # max_digits=7 - максимальное количество цифр в числе (вместе с дробной частью)
    # decimal_places=2 - два числа после запятой
    price = models.DecimalField(verbose_name='Цена книги', max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'

