from django.contrib import admin

from store.models import Book, UserBookRelation


class BookAdmin(admin.ModelAdmin):
    # список отображаемых столбцов в админ-панели
    list_display = ('id', 'name', 'price', 'author_name', 'owner')
    # список полей на которые можно кликнуть - для редактирования
    list_display_links = ('id', 'name', 'price', 'author_name', 'owner')
    # список полей - ко которым можно вести поиск
    search_fields = ('name', 'author_name')


class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'like', 'is_bookmarks', 'rate')
    list_display_links = ('like', 'is_bookmarks', 'rate')
    search_fields = ('user', 'book')


# регистрируем в админке - модель Book
# регистрируем класс отображения в админке - BookAdmin
admin.site.register(Book, BookAdmin)

admin.site.register(UserBookRelation, UserBookRelationAdmin)
