from src.main import Product, Category


def test_product_creation() -> None:
    product = Product("iPhone 15", "512GB, Gray space", 210000.0, 8)

    assert product.name == "iPhone 15"
    assert product.description == "512GB, Gray space"
    assert product.price == 210000.0
    assert product.quantity == 8

    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


def test_category_creation() -> None:
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("iPhone 15", "512GB, Gray space", 210000.0, 8)
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [product1, product2])

    assert category.name == "Смартфоны"
    assert category.description == "Смартфоны для удобства жизни"
    assert len(category.products) == 2

    assert Category.category_count == 1
    assert Category.product_count == 2


def test_category_counters() -> None:
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("iPhone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)

    Category("Смартфоны", "Смартфоны для удобства жизни", [product1, product2])
    Category("Телевизоры", "Телевизоры для просмотра фильмов", [product3, product4])

    assert Category.category_count == 3
    assert Category.product_count == 6


def test_add_product_to_category() -> None:
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    category = Category("Смартфоны", "Смартфоны для удобства жизни", [product1])

    product2 = Product("iPhone 15", "512GB, Gray space", 210000.0, 8)
    category.products.append(product2)

    assert len(category.products) == 2
    assert product2 in category.products
