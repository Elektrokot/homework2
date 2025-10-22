import pytest

from src.product import Product


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
    assert product.quantity == 5


def test_new_product_update(sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет обновление существующего продукта через класс-метод new_product.
    """
    product_data = {"name": "iPhone 15", "description": "512GB, Gray space", "price": 200000.0, "quantity": 3}
    Product.new_product(product_data)
    assert sample_product.quantity == 11  # Количество должно сложиться
    assert sample_product.price == 210000.0  # Выбирается максимальная цена


def test_add_product(sample_category, sample_product_3):  # type: ignore[no-untyped-def]
    """
    Проверяет добавление нового продукта в категорию.
    """
    new_product = sample_product_3
    sample_category.add_product(new_product)
    assert sample_category.product_count == 22


def test_products_property(sample_category, sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет вывод списка продуктов через геттер products.
    """
    expected_output = "iPhone 15, 210000.0 руб. Остаток: 8 шт."
    assert sample_category.products == expected_output


# Тесты для метода __add__
def test_smartphone_addition(smartphone1, smartphone2):  # type: ignore[no-untyped-def]
    """
    Проверяет сложение двух смартфонов.
    """
    total_cost = smartphone1 + smartphone2
    assert total_cost == 180000.0 * 5 + 210000.0 * 8


def test_lawn_grass_addition(grass1, grass2):  # type: ignore[no-untyped-def]
    """
    Проверяет сложение двух газонных трав.
    """
    total_cost = grass1 + grass2
    assert total_cost == 500.0 * 20 + 450.0 * 15


def test_invalid_addition(smartphone1, grass1):  # type: ignore[no-untyped-def]
    """
    Проверяет, что сложение объектов разных классов вызывает TypeError.
    """
    with pytest.raises(TypeError, match="Нельзя складывать объекты разных типов."):
        smartphone1 + grass1


# Тесты для метода add_product
def test_add_valid_product(smartphone1, sample_category_2):  # type: ignore[no-untyped-def]
    """
    Проверяет добавление корректного продукта в категорию.
    """
    sample_category_2.add_product(smartphone1)
    assert len(sample_category_2.get_products()) == 1


def test_add_invalid_product(sample_category_2):  # type: ignore[no-untyped-def]
    """
    Проверяет, что добавление некорректного объекта вызывает TypeError.
    """
    invalid_object = "Not a product"
    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников."):
        sample_category_2.add_product(invalid_object)  # type: ignore[no-untyped-def]


def test_product_creation_with_zero_quantity():  # type: ignore[no-untyped-def]
    """
    Проверяет, что при создании продукта с нулевым количеством выбрасывается ValueError.
    """
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Тестовый товар", "Описание", 1000.0, 0)
