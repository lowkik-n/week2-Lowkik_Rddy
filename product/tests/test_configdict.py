from decimal import Decimal

from product.models.product import Product
from product.models.user import User
from product.schemas.order_schema import OrderCreate
from product.schemas.product_schema import ProductCreate, ProductResponse
from product.schemas.user_schema import UserResponse


def test_product_create_accepts_database_style_aliases() -> None:
    product = ProductCreate(
        ProductName="Wireless Mouse",
        Description="Test mouse",
        CategoryID=1,
        Price=Decimal("25.50"),
        AvailableQuantity=20,
    )

    assert product.product_name == "Wireless Mouse"
    assert product.category_id == 1
    assert product.price == Decimal("25.50")
    assert product.available_quantity == 20


def test_product_create_accepts_python_field_names() -> None:
    product = ProductCreate(
        product_name="Mechanical Keyboard",
        description="Test keyboard",
        category_id=1,
        price=Decimal("75.00"),
        available_quantity=10,
    )

    assert product.product_name == "Mechanical Keyboard"
    assert product.category_id == 1


def test_user_response_reads_sqlalchemy_attributes() -> None:
    user = User(
        UserID=7,
        Name="Config User",
        Email="config@example.com",
        Password="hidden",
        Mobile="9876543212",
        Role="customer",
    )

    response = UserResponse.model_validate(user)

    assert response.user_id == 7
    assert response.name == "Config User"
    assert response.email == "config@example.com"
    assert response.mobile == "9876543212"


def test_product_response_reads_sqlalchemy_attributes() -> None:
    product = Product(
        ProductID=5,
        ProductName="Monitor",
        Description="Test monitor",
        CategoryID=1,
        Price=Decimal("150.00"),
        AvailableQuantity=4,
        ProductUrl=None,
    )

    response = ProductResponse.model_validate(product)

    assert response.product_id == 5
    assert response.product_name == "Monitor"
    assert response.price == Decimal("150.00")


def test_order_create_normalizes_payment_method() -> None:
    order = OrderCreate(
        UserID=1,
        PaymentMethod=" CARD ",
    )

    assert order.user_id == 1
    assert order.payment_method == "card"


def test_schema_configdict_values() -> None:
    assert ProductCreate.model_config["populate_by_name"] is True
    assert ProductResponse.model_config["from_attributes"] is True
    assert UserResponse.model_config["from_attributes"] is True
