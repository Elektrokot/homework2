import pytest

from src.category import Category, CategoryIterator


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


def test_order_creation(sample_order):  # type: ignore[no-untyped-def]
    """
    Проверяет корректность создания заказа.
    """
    assert sample_order.product.name == "iPhone 15"
    assert sample_order.quantity == 2
    assert sample_order.total_cost() == 210000.0 * 2


def test_order_total_cost(sample_order):  # type: ignore[no-untyped-def]
    """
    Проверяет метод total_cost для заказа.
    """
    assert sample_order.total_cost() == 210000.0 * 2


def test_order_str_representation(sample_order):  # type: ignore[no-untyped-def]
    """
    Проверяет строковое представление заказа.
    """
    expected_output = "Товар: iPhone 15, количество: 2, итоговая стоимость: 420000.0 руб."
    assert str(sample_order) == expected_output


def test_category_middle_price_with_products(sample_product, sample_product_2):  # type: ignore[no-untyped-def]
    """
    Проверяет корректность вычисления средней цены товаров в категории.
    """
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [sample_product, sample_product_2])
    expected_average = (sample_product.price + sample_product_2.price) / 2
    assert category.middle_price() == expected_average


def test_category_middle_price_empty():  # type: ignore[no-untyped-def]
    """
    Проверяет, что при отсутствии товаров в категории метод middle_price возвращает 0.
    """
    category = Category("Пустая категория", "Категория без продуктов", [])
    assert category.middle_price() == 0.0
