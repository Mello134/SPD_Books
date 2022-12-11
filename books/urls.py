"""books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter  # маршрутизатор rest
from store.views import BookViewSet, my_auth, UserBooksRelationView  # наше представление api

# создали переменную роутер
router = SimpleRouter()

# в роутер добавим наше представление
router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBooksRelationView)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', my_auth, name='my_auth'),
]

# добавляем в urlpatterns, url-ы нашего роутера
urlpatterns += router.urls
