from django.contrib import admin

from store.models import Book


class BookAdmin(admin.ModelAdmin):
    # список отображаемых столбцов в админ-панели
    list_display = ('id', 'name', 'price', 'author_name')
    # список полей на которые можно кликнуть - для редактирования
    list_display_links = ('id', 'name', 'price', 'author_name')
    # список полей - ко которым можно вести поиск
    search_fields = ('name', 'author_name')


# регистрируем в админке - модель Book
# регистрируем класс отображения в админке - BookAdmin
admin.site.register(Book, BookAdmin)
