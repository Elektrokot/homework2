from abc import ABC, abstractmethod

from .exceptions import ProductQuantityException
from .product import Product


class Orderable(ABC):
    """
    Абстрактный класс для заказов.
    """

    @abstractmethod
    def total_cost(self) -> float:
        """
        Возвращает итоговую стоимость.
        """
        pass


class Order(Orderable):
    """
    Класс для заказов.
    """

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        self._process_addition()

    def _process_addition(self) -> None:
        """
        Обработка добавления товара в заказ с проверкой количества.
        """
        try:
            if self.quantity <= 0:
                raise ProductQuantityException()
            print("Товар добавлен в заказ")
        except ProductQuantityException as e:
            print(e.message)
        finally:
            print("Обработка добавления товара завершена")

    def total_cost(self) -> float:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f"Товар: {self.product.name}, количество: {self.quantity}, итоговая стоимость: {self.total_cost()} руб."


class Category(Orderable):
    """
    Класс Категории товаров.
    """

    name: str
    description: str
    __products: list[Product]  # Приватный атрибут списка продуктов
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """
        Метод для добавления продукта в категорию.
        При этом увеличивается счетчик продуктов.
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников.")

        try:
            if product.quantity <= 0:
                raise ProductQuantityException()
            self.__products.append(product)
            Category.product_count += 1
            print("Товар добавлен в категорию")
        except ProductQuantityException as e:
            print(e.message)
        else:
            # Выполняется только если не было исключений
            pass
        finally:
            print("Обработка добавления товара завершена")

    @property
    def products(self) -> str:
        """
        Геттер для приватного атрибута __products.
        Возвращает строку с информацией о продуктах в формате:
        "Название продукта, X руб. Остаток: X шт.\n".
        """
        return "\n".join(
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self.__products
        )

    def get_products(self) -> list[Product]:
        """
        Метод для получения списка продуктов категории.
        """
        return self.__products

    def total_cost(self) -> float:
        """
        Возвращает общую стоимость всех товаров в категории.
        """
        total_cost = sum(product.price * product.quantity for product in self.__products)
        return total_cost

    def middle_price(self) -> float:
        """
        Метод для вычисления средней цены товаров в категории.
        В случае отсутствия товаров возвращает 0.
        """
        try:
            total_price = sum(product.price for product in self.__products)
            count = len(self.__products)
            return total_price / count
        except ZeroDivisionError:
            return 0.0

    def __str__(self) -> str:
        """
        Строковое представление категории.
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> "CategoryIterator":
        """
        Возвращает итератор для перебора товаров категории.
        """
        return CategoryIterator(self)


class CategoryIterator:
    """
    Вспомогательный класс для итерации по товарам категории.
    """

    def __init__(self, category: "Category") -> None:
        """
        Инициализирует итератор для заданной категории.
        """
        self.__category = category
        self.__index = 0  # Индекс текущего товара

    def __iter__(self) -> "CategoryIterator":
        """
        Возвращает сам итератор.
        """
        return self

    def __next__(self) -> "Product":
        """
        Возвращает следующий товар категории.
        Если товаров больше нет, вызывает StopIteration.
        """
        products = self.__category.get_products()  # Получаем список товаров категории
        if self.__index < len(products):
            product = products[self.__index]
            self.__index += 1
            return product
        else:
            raise StopIteration
