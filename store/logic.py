from django.db.models import Avg
from store.models import UserBookRelation


# получение рейтинга
def set_rating(book):
    # book - это определённая книга
    # aggregate - сами расчёты
    # class(models.py) UserBookRelation/ rate это поле - UserBookRelation
    rating = UserBookRelation.objects.filter(book=book).aggregate(rating=Avg('rate')).get('rating')
    # записываем в поле rating- переменную rating
    book.rating = rating
    book.save()  # сохраняем книгу
