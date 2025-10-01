from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.
    """

    name: str
    description: str
    _price: float  # Приватный атрибут цены
    quantity: int

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """
        Инициализация базовых атрибутов продукта.
        """
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    @abstractmethod
    def price(self) -> float:
        """
        Абстрактный геттер для цены.
        """
        pass

    @price.setter
    @abstractmethod
    def price(self, new_price: float) -> None:
        """
        Абстрактный сеттер для цены.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Абстрактный метод для строкового представления продукта.
        """
        pass

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> float:
        """
        Абстрактный метод для сложения двух продуктов.
        """
        pass


class LoggerMixin:
    """
    Миксин для логирования создания объекта.
    """

    def __init__(self, *args: Any) -> None:
        """
        Логирует создание объекта с указанием класса и параметров.
        """
        print(f"{self.__class__.__name__}{args}")
        super().__init__(*args)  # type: ignore[call-arg]

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта.
        """
        name = getattr(self, "name", "Unknown")
        description = getattr(self, "description", "Unknown")
        price = getattr(self, "_price", 0.0)
        quantity = getattr(self, "quantity", 0)
        return f"{self.__class__.__name__}({name}, {description}, {price}, {quantity})"


class Product(BaseProduct, LoggerMixin):
    """
    Базовый класс для продуктов с миксином логирования.
    """

    all_products: list["Product"] = []  # Статический атрибут для хранения всех продуктов

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)
        Product.all_products.append(self)  # Добавляем продукт в общий список

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута цены."""
        return self._price

    @price.setter
    def price(self, new_price: float):  # type: ignore[no-untyped-def]
        """
        Сеттер для приватного атрибута цены.
        Проверяет корректность новой цены и при необходимости запрашивает подтверждение пользователя.
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self._price:  # Проверяем, понижается ли цена
            confirmation = input("Цена понижается. Вы уверены? (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено.")
                return

        self._price = new_price

    @classmethod
    def new_product(cls, product_data: Dict[str, Any]) -> "Product":
        """
        Класс-метод для создания нового продукта из словаря данных.
        Если продукт уже существует, объединяет количество и выбирает более высокую цену.
        """
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        # Проверяем все существующие продукты
        for product in cls.all_products:
            if product.name == name:  # Если найден продукт с таким же именем
                product.quantity += quantity  # Обновляем количество
                if price > product.price:  # Выбираем более высокую цену
                    product.price = price
                print(f"Продукт {name} обновлен: новое количество - {product.quantity}, цена - {product.price}")
                return product  # Возвращаем обновленный продукт

        # Если продукт не найден, создаем новый
        new_product = cls(name, description, price, quantity)
        print(f"Создан новый продукт: {name}")
        return new_product

    def __str__(self) -> str:
        """
        Строковое представление продукта.
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "BaseProduct") -> float:
        """
        Магический метод для сложения двух продуктов.
        Возвращает полную стоимость всех товаров на складе.
        """
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать объекты разных типов.")

        total_cost_self = self.price * self.quantity
        total_cost_other = other.price * other.quantity
        return total_cost_self + total_cost_other


class Smartphone(Product):
    """
    Дочерний класс: Смартфоны.
    Родительский класс: Продукты.
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """
    Дочерний класс: Газоны.
    Родительский класс: Продукты.
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
