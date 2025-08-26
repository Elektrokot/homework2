import pytest

from src.main import Category, CategoryIterator, Product


# Тесты для класса CategoryIterator
def test_category_iterator(sample_product, sample_product_2):  # type: ignore[no-untyped-def]
    """
    Проверяет корректность работы класса CategoryIterator.
    """
    # Создание категории
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [sample_product, sample_product_2])

    # Создание итератора
    iterator = CategoryIterator(category)

    # Проверка первого товара
    assert next(iterator) == sample_product

    # Проверка второго товара
    assert next(iterator) == sample_product_2

    # Проверка завершения итерации
    with pytest.raises(StopIteration):
        next(iterator)


def test_empty_category_iterator() -> None:
    """
    Проверяет работу итератора для пустой категории.
    """
    # Создание пустой категории
    category = Category("Пустая категория", "Описание пустой категории", [])

    # Создание итератора
    iterator = CategoryIterator(category)

    # Проверка завершения итерации
    with pytest.raises(StopIteration):
        next(iterator)


def test_category_iteration_with_for_loop(sample_product, sample_product_2):  # type: ignore[no-untyped-def]
    """
    Проверяет возможность использования цикла for для перебора товаров категории.
    """
    # Создание категории
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [sample_product, sample_product_2])

    # Перебор товаров через цикл for
    products_in_category = []
    for product in category:
        products_in_category.append(product)

    # Проверка, что все товары перебраны
    assert products_in_category == [sample_product, sample_product_2]


def test_category_iter_method(sample_product, sample_product_2):  # type: ignore[no-untyped-def]
    """
    Проверяет, что метод __iter__ категории возвращает корректный итератор.
    """
    # Создание категории
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [sample_product, sample_product_2])

    # Получение итератора через метод __iter__
    iterator = iter(category)

    # Проверка, что это экземпляр CategoryIterator
    assert isinstance(iterator, CategoryIterator)

    # Проверка первого товара
    assert next(iterator) == sample_product

    # Проверка второго товара
    assert next(iterator) == sample_product_2

    # Проверка завершения итерации
    with pytest.raises(StopIteration):
        next(iterator)


def test_category_creation(sample_product, sample_product_2):  # type: ignore[no-untyped-def]
    """
    Проверяет корректность создания объекта Category.
    """
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [sample_product, sample_product_2])

    assert category.name == "Смартфоны"
    assert category.description == "Смартфоны для удобства жизни"
    assert len(category.get_products()) == 2

    assert Category.category_count == 5
    assert Category.product_count == 8


def test_category_counters(  # type: ignore[no-untyped-def]
    sample_product, sample_product_2, sample_product_3, sample_product_4
):
    """
    Проверяет корректность счётчика категорий и продуктов в Category.
    """
    Category("Смартфоны", "Смартфоны для удобства жизни", [sample_product, sample_product_2])
    Category("Телевизоры", "Телевизоры для просмотра фильмов", [sample_product_3, sample_product_4])

    assert Category.category_count == 7
    assert Category.product_count == 12


def test_add_product_to_category(sample_product, sample_product_2):  # type: ignore[no-untyped-def]
    # Создаем продукты
    product1 = sample_product
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [product1])

    product2 = sample_product_2

    # Добавляем продукт через метод add_product
    category.add_product(product2)

    # Проверяем, что продукт добавлен
    assert len(category.get_products()) == 2  # Количество продуктов должно быть 2
    assert product2 in category.get_products()  # Продукт должен быть в списке


def test_category_str_representation(sample_product, sample_product_2):  # type: ignore[no-untyped-def]
    """
    Проверяет строковое представление категории.
    """
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [sample_product, sample_product_2])
    assert str(category) == "Смартфоны, количество продуктов: 13 шт."


def test_category_products_property(sample_product, sample_product_2):  # type: ignore[no-untyped-def]
    """
    Проверяет работу свойства products.
    """
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [sample_product, sample_product_2])
    expected_output = "\n".join([str(sample_product), str(sample_product_2)])
    assert category.products == expected_output


# Тесты для класса Product
def test_product_creation(sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет корректность создания объекта Product.
    """
    assert sample_product.name == "iPhone 15"
    assert sample_product.description == "512GB, Gray space"
    assert sample_product.price == 210000.0
    assert sample_product.quantity == 8


def test_price_setter_valid(sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет установку новой цены (валидное значение).
    """
    sample_product.price = 220000.0
    assert sample_product.price == 220000.0


def test_product_addition(sample_product, sample_product_2):  # type: ignore[no-untyped-def]
    """
    Проверяет корректность работы метода __add__.
    """
    total_cost = sample_product + sample_product_2
    assert total_cost == 210000.0 * 8 + 180000.0 * 5


def test_product_addition_with_invalid_type(sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет обработку ошибок при попытке сложить продукт с объектом другого типа.
    """
    # Попытка сложить продукт со строкой
    with pytest.raises(TypeError, match="Нельзя складывать объекты разных типов."):
        sample_product + "invalid"  # type: ignore[no-untyped-def]

    # Попытка сложить продукт с числом
    with pytest.raises(TypeError, match="Нельзя складывать объекты разных типов."):
        sample_product + 123  # type: ignore[no-untyped-def]

    # Попытка сложить продукт с None
    with pytest.raises(TypeError, match="Нельзя складывать объекты разных типов."):
        sample_product + None  # type: ignore[no-untyped-def]


def test_price_setter_invalid(sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет установку некорректной цены (отрицательное значение).
    """
    sample_product.price = -100
    assert sample_product.price == 210000.0  # Цена не должна измениться


def test_price_setter_cancel(monkeypatch, sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет подтверждение пользователя при понижении цены.
    """
    monkeypatch.setattr("builtins.input", lambda _: "n")  # Отменяем действие
    sample_product.price = 200000.0
    assert sample_product.price == 210000.0  # Цена не должна измениться


def test_price_setter_confirmation(monkeypatch, sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет подтверждение пользователя при понижении цены.
    """
    monkeypatch.setattr("builtins.input", lambda _: "y")  # Подтверждаем действие
    sample_product.price = 200000.0
    assert sample_product.price == 200000.0  # Цена должна измениться


def test_new_product_creation():  # type: ignore[no-untyped-def]
    """
    Проверяет создание нового продукта через класс-метод new_product.
    """
    product_data = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5,
    }
    product = Product.new_product(product_data)
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.price == 180000.0
    assert product.quantity == 10


def test_new_product_update(sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет обновление существующего продукта через класс-метод new_product.
    """
    product_data = {"name": "iPhone 15", "description": "512GB, Gray space", "price": 200000.0, "quantity": 3}
    Product.new_product(product_data)
    assert sample_product.quantity == 8  # Количество должно сложиться
    assert sample_product.price == 210000.0  # Выбирается максимальная цена


def test_add_product(sample_category, sample_product_3):  # type: ignore[no-untyped-def]
    """
    Проверяет добавление нового продукта в категорию.
    """
    new_product = sample_product_3
    sample_category.add_product(new_product)
    assert sample_category.product_count == 20


def test_products_property(sample_category, sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет вывод списка продуктов через геттер products.
    """
    expected_output = "iPhone 15, 210000.0 руб. Остаток: 8 шт."
    assert sample_category.products == expected_output
