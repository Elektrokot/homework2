from typing import Dict, Any


class Product:
    name: str
    description: str
    __price: float  # Приватный атрибут цены
    quantity: int
    all_products: list["Product"] = []  # Статический атрибут для хранения всех продуктов

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        Product.all_products.append(self)  # Добавляем продукт в общий список

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float):  # type: ignore[no-untyped-def]
        """
        Сеттер для приватного атрибута цены.
        Проверяет корректность новой цены и при необходимости запрашивает подтверждение пользователя.
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:  # Проверяем, понижается ли цена
            confirmation = input("Цена понижается. Вы уверены? (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено.")
                return

        self.__price = new_price

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

    def __add__(self, other: "Product") -> float:
        """
        Магический метод для сложения двух продуктов.
        Возвращает полную стоимость всех товаров на складе.
        """
        if not isinstance(other, Product):
            raise TypeError("Нельзя складывать объекты разных типов.")

        total_cost_self = self.price * self.quantity
        total_cost_other = other.price * other.quantity
        return total_cost_self + total_cost_other


class Category:
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


# if __name__ == "__main__":  # pragma: no cover
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     category1 = Category(
#         "Смартфоны",
#         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#         [product1, product2, product3],
#     )
#
#     print(category1.products)
#     product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
#     category1.add_product(product4)
#     print(category1.products)
#     print(category1.product_count)
#
#     new_product = Product.new_product(
#         {
#             "name": "Samsung Galaxy S23 Ultra",
#             "description": "256GB, Серый цвет, 200MP камера",
#             "price": 180000.0,
#             "quantity": 5,
#         }
#     )
#
#     print(new_product.name)
#     print(new_product.description)
#     print(new_product.price)
#     print(new_product.quantity)
#
#     new_product.price = 800
#     print(new_product.price)
#
#     new_product.price = -100
#     print(new_product.price)
#     new_product.price = 0
#     print(new_product.price)


if __name__ == "__main__":  # pragma: no cover
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)

    # Перебор товаров категории
    print("Товары категории:")
    for product in category1:
        print(product)

    # Проверка на ошибку при сложении разных типов
    # print(product1 + 123)
