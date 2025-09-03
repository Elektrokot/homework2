import json

import pytest

from src.main import Category, LawnGrass, Product, Smartphone


@pytest.fixture
def valid_json_file(tmp_path):  # type: ignore[no-untyped-def]
    """
    Создает временный JSON-файл с корректными данными.
    """
    data = [
        {
            "name": "Смартфоны",
            "description": "Смартфоны для удобства жизни",
            "products": [
                {
                    "name": "Samsung Galaxy S23 Ultra",
                    "description": "256GB, Серый цвет, 200MP камера",
                    "price": 180000.0,
                    "quantity": 5,
                },
                {"name": "iPhone 15", "description": "512GB, Gray space", "price": 210000.0, "quantity": 8},
            ],
        },
        {
            "name": "Телевизоры",
            "description": "Телевизоры для просмотра фильмов",
            "products": [
                {"name": '55" QLED 4K', "description": "Фоновая подсветка", "price": 123000.0, "quantity": 7}
            ],
        },
    ]

    file_path = tmp_path / "test_data.json"
    with open(file_path, "w", encoding="UTF-8") as f:
        json.dump(data, f)

    return file_path


@pytest.fixture
def invalid_json_file(tmp_path):  # type: ignore[no-untyped-def]
    """
    Создает временный JSON-файл с некорректными данными.
    """
    file_path = tmp_path / "invalid_data.json"
    with open(file_path, "w", encoding="UTF-8") as f:
        f.write("invalid json")

    return file_path


@pytest.fixture
def sample_product() -> Product:
    """
    Фикстура для создания экземпляра класса Product.
    """
    Product.all_products = list()
    return Product("iPhone 15", "512GB, Gray space", 210000.0, 8)


@pytest.fixture
def sample_product_2() -> Product:
    """
    Фикстура для создания экземпляра класса Product.
    """
    Product.all_products = list()
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


@pytest.fixture
def sample_product_3() -> Product:
    """
    Фикстура для создания экземпляра класса Product.
    """
    Product.all_products = list()
    return Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)


@pytest.fixture
def sample_product_4() -> Product:
    """
    Фикстура для создания экземпляра класса Product.
    """
    Product.all_products = list()
    return Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)


@pytest.fixture
def sample_category(sample_product) -> Category:  # type: ignore[no-untyped-def]
    """
    Фикстура для создания экземпляра класса Category.
    Использует фикстуру sample_product для добавления продукта в категорию.
    """
    Category.category_count = 0
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [])
    category.add_product(sample_product)
    return category


@pytest.fixture
def sample_category_2() -> Category:  # type: ignore[no-untyped-def]
    """
    Фикстура для создания экземпляра класса Category.
    """
    Category.category_count = 0
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [])
    return category


@pytest.fixture
def smartphone1() -> Smartphone:
    """
    Фикстура для создания экземпляра класса Smartphone.
    """
    Product.all_products = list()
    return Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
    )


@pytest.fixture
def smartphone2() -> Smartphone:
    """
    Фикстура для создания экземпляра класса Smartphone.
    """
    Product.all_products = list()
    return Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")


@pytest.fixture
def grass1() -> LawnGrass:
    """
    Фикстура для создания экземпляра класса LawnGrass.
    """
    Product.all_products = list()
    return LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")


@pytest.fixture
def grass2() -> LawnGrass:
    """
    Фикстура для создания экземпляра класса LawnGrass.
    """
    Product.all_products = list()
    return LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")
