from src.main import Category, Product


def test_category_creation() -> None:
    """
    Проверяет корректность создания объекта Category.
    """
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("iPhone 15", "512GB, Gray space", 210000.0, 8)
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [product1, product2])

    assert category.name == "Смартфоны"
    assert category.description == "Смартфоны для удобства жизни"
    assert len(category.get_products()) == 2

    assert Category.category_count == 1
    assert Category.product_count == 2


def test_category_counters() -> None:
    """
    Проверяет корректность счётчика категорий и продуктов в Category.
    """
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("iPhone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)

    Category("Смартфоны", "Смартфоны для удобства жизни", [product1, product2])
    Category("Телевизоры", "Телевизоры для просмотра фильмов", [product3, product4])

    assert Category.category_count == 3
    assert Category.product_count == 6


def test_add_product_to_category() -> None:
    # Создаем продукты
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [product1])

    product2 = Product("iPhone 15", "512GB, Gray space", 210000.0, 8)

    # Добавляем продукт через метод add_product
    category.add_product(product2)

    # Проверяем, что продукт добавлен
    assert len(category.get_products()) == 2  # Количество продуктов должно быть 2
    assert product2 in category.get_products()  # Продукт должен быть в списке


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


def test_add_product(sample_category, sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет добавление нового продукта в категорию.
    """
    new_product = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    sample_category.add_product(new_product)
    assert sample_category.product_count == 10


def test_products_property(sample_category, sample_product):  # type: ignore[no-untyped-def]
    """
    Проверяет вывод списка продуктов через геттер products.
    """
    expected_output = "iPhone 15, 210000.0 руб. Остаток: 8 шт."
    assert sample_category.products == expected_output
