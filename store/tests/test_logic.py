from unittest import TestCase

from store.logic import operations  # наша функция


# наш тест на основе базового TestCase
class LogicTestCase(TestCase):
    def test_plus(self):  # метод внутри теста
        # подставляем значения abc
        # def operations (a, b, c) - прописана в другой файле
        result = operations(6, 13, '+')
        # (то что мы ожидаем, результат)
        self.assertEqual(19, result)

    def test_minus(self):
        result = operations(6, 13, '-')
        # (то что мы ожидаем, результат)
        self.assertEqual(-7, result)

    def test_multiply(self):
        result = operations(6, 13, '*')
        # (то что мы ожидаем, результат)
        self.assertEqual(78, result)
