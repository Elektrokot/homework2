import pytest

from src.main import Category, Product
from src.utils import create_objects_from_json, read_json


# Тесты для функции read_json
def test_read_json_valid(valid_json_file):  # type: ignore[no-untyped-def]
    """
    Проверяет корректное чтение данных из валидного JSON-файла.
    """
    data = read_json(valid_json_file)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Смартфоны"
    assert data[1]["name"] == "Телевизоры"


def test_read_json_file_not_found() -> None:
    """
    Проверяет обработку ошибки при отсутствии файла.
    """
    with pytest.raises(FileNotFoundError):
        read_json("non_existent_file.json")


def test_read_json_invalid(invalid_json_file):  # type: ignore[no-untyped-def]
    """
    Проверяет обработку ошибки при некорректном JSON.
    """
    with pytest.raises(ValueError):
        read_json(invalid_json_file)


# Тесты для функции create_objects_from_json
def test_create_objects_from_json(valid_json_file):  # type: ignore[no-untyped-def]
    """
    Проверяет корректное создание объектов Category и Product из JSON.
    """
    data = read_json(valid_json_file)
    categories = create_objects_from_json(data)

    assert len(categories) == 2
    assert all(isinstance(category, Category) for category in categories)

    # Проверяем первую категорию
    category1 = categories[0]
    assert category1.name == "Смартфоны"
    assert category1.description == "Смартфоны для удобства жизни"
    assert len(category1.get_products()) == 2  # Используем метод get_products
    assert all(isinstance(product, Product) for product in category1.get_products())

    # Проверяем второй продукт первой категории
    product2 = category1.get_products()[1]  # Используем метод get_products
    assert product2.name == "iPhone 15"
    assert product2.price == 210000.0
    assert product2.quantity == 8

    # Проверяем вторую категорию
    category2 = categories[1]
    assert category2.name == "Телевизоры"
    assert len(category2.get_products()) == 1  # Используем метод get_products
    assert category2.get_products()[0].name == '55" QLED 4K'


def test_create_objects_from_empty_json() -> None:
    """
    Проверяет обработку пустого JSON.
    """
    data: list = []
    categories = create_objects_from_json(data)
    assert len(categories) == 0
