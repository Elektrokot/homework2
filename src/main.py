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


class LoggerMixin(BaseProduct, ABC):
    """
    Миксин для логирования создания объекта.
    """

    def __init__(self, *args: Any) -> None:
        """
        Логирует создание объекта с указанием класса и параметров.
        """
        print(f"{self.__class__.__name__}{args}")
        super().__init__(*args)

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта.
        """
        return f"{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})"


class Product(LoggerMixin, BaseProduct):
    """
    Базовый класс для продуктов с миксином логирования.
    """

    all_products: list["Product"] = []  # Статический атрибут для хранения всех продуктов

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
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

    def __init__(self, product: BaseProduct, quantity: int):
        self.product = product
        self.quantity = quantity

    def total_cost(self) -> float:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f"Товар: {self.product.name}, количество: {self.quantity}, итоговая стоимость: {self.total_cost()} руб."


class Category:
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
        self.__products.append(product)
        Category.product_count += 1

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


if __name__ == "__main__":  # pragma: no cover
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)

    order = Order(product2, 2)
    print(order)


# if __name__ == "__main__":  # pragma: no cover
# smartphone1 = Smartphone(
#     "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
# )
# smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
# smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")
#
# print(smartphone1.name)
# print(smartphone1.description)
# print(smartphone1.price)
# print(smartphone1.quantity)
# print(smartphone1.efficiency)
# print(smartphone1.model)
# print(smartphone1.memory)
# print(smartphone1.color)
#
# print(smartphone2.name)
# print(smartphone2.description)
# print(smartphone2.price)
# print(smartphone2.quantity)
# print(smartphone2.efficiency)
# print(smartphone2.model)
# print(smartphone2.memory)
# print(smartphone2.color)
#
# print(smartphone3.name)
# print(smartphone3.description)
# print(smartphone3.price)
# print(smartphone3.quantity)
# print(smartphone3.efficiency)
# print(smartphone3.model)
# print(smartphone3.memory)
# print(smartphone3.color)
#
# grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
# grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")
#
# print(grass1.name)
# print(grass1.description)
# print(grass1.price)
# print(grass1.quantity)
# print(grass1.country)
# print(grass1.germination_period)
# print(grass1.color)
#
# print(grass2.name)
# print(grass2.description)
# print(grass2.price)
# print(grass2.quantity)
# print(grass2.country)
# print(grass2.germination_period)
# print(grass2.color)
#
# smartphone_sum = smartphone1 + smartphone2
# print(smartphone_sum)
#
# grass_sum = grass1 + grass2
# print(grass_sum)
#
# try:
#     invalid_sum = smartphone1 + grass1
# except TypeError:
#     print("Возникла ошибка TypeError при попытке сложения")
# else:
#     print("Не возникла ошибка TypeError при попытке сложения")
#
# category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
# category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])
#
# category_smartphones.add_product(smartphone3)
#
# print(category_smartphones.products)
#
# print(Category.product_count)
#
# try:
#     category_smartphones.add_product("Not a product")  # arg-type: ignore[no-untyped-def]
# except TypeError:
#     print("Возникла ошибка TypeError при добавлении не продукта")
# else:
#     print("Не возникла ошибка TypeError при добавлении не продукта")
