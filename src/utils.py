import json
import os
from typing import Any

from src.main import Product, Category


def read_json(path: str) -> list:
    """
    Читает JSON файл и возвращает его содержимое в виде словаря.
    """
    full_path = os.path.abspath(path)
    try:
        with open(full_path, "r", encoding="UTF-8") as file:
            data: list = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {full_path} не найден.")
    except json.JSONDecodeError:
        raise ValueError(f"Ошибка при декодировании JSON из файла {full_path}.")


def create_objects_from_json(data: list) -> list[Category]:
    """
    Создает объекты классов Product и Category из данных JSON.
    """
    categories = []
    for category_data in data:
        # Создаем список объектов Product
        products = [
            Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            for product_data in category_data["products"]
        ]

        # Создаем объект Category
        category = Category(name=category_data["name"], description=category_data["description"], products=products)

        categories.append(category)

    return categories


if __name__ == "__main__":

    data: list = read_json("../data/products.json")

    categories = create_objects_from_json(data)

    for category in categories:
        print(f"Категория: {category.name}")
        print(f"Описание: {category.description}")
        print("Товары:")
        for product in category.products:
            print(f"  - {product.name}, Цена: {product.price}, Количество: {product.quantity}")
        print()
