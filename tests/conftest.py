import pytest
import json


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
