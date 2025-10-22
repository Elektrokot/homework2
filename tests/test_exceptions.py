def test_product_quantity_exception_creation():  # type: ignore[no-untyped-def]
    """
    Проверяет создание исключения ProductQuantityException с сообщением по умолчанию.
    """
    from src.exceptions import ProductQuantityException

    exception = ProductQuantityException()
    assert str(exception) == "Товар с нулевым количеством не может быть добавлен"
    assert exception.message == "Товар с нулевым количеством не может быть добавлен"


def test_product_quantity_exception_custom_message():  # type: ignore[no-untyped-def]
    """
    Проверяет создание исключения ProductQuantityException с пользовательским сообщением.
    """
    from src.exceptions import ProductQuantityException

    custom_message = "Пользовательское сообщение об ошибке"
    exception = ProductQuantityException(custom_message)
    assert str(exception) == custom_message
    assert exception.message == custom_message


def test_category_add_product_with_zero_quantity_raises_exception():  # type: ignore[no-untyped-def]
    """
    Проверяет, что при добавлении продукта с нулевым количеством в категорию вызывается ProductQuantityException.
    """
    from src.category import Category
    from src.product import Product

    # Создаем продукт с нулевым количеством
    product = Product("Тест", "Тестовый продукт", 1000.0, 1)
    product.quantity = 0  # Устанавливаем количество в 0

    category = Category("Тестовая категория", "Описание", [])

    # Проверяем, что при добавлении продукта с нулевым количеством вызывается исключение
    # Так как исключение обрабатывается внутри метода, проверим вывод на печать
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        category.add_product(product)

    output = f.getvalue()
    assert "Товар с нулевым количеством не может быть добавлен" in output
    assert "Обработка добавления товара завершена" in output


def test_order_creation_with_zero_quantity_raises_exception():  # type: ignore[no-untyped-def]
    """
    Проверяет, что при создании заказа с нулевым количеством вызывается ProductQuantityException.
    """
    from src.category import Order
    from src.product import Product

    product = Product("Тест", "Тестовый продукт", 1000.0, 5)

    # Создаем заказ с нулевым количеством
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        Order(product, 0)

    output = f.getvalue()
    assert "Товар с нулевым количеством не может быть добавлен" in output
    assert "Обработка добавления товара завершена" in output
