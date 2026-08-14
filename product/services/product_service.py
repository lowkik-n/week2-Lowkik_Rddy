from sqlalchemy.orm import Session

from product.models.category import Category
from product.models.product import Product
from product.repositories import product_repository
from product.schemas.product_schema import ProductCreate
from product.repositories import (
    category_repository,
    product_repository,
)



def create_product(
    db: Session,
    product_data: ProductCreate,
) -> Product:
    category = (
        db.query(Category)
        .filter(
            Category.CategoryID == product_data.category_id
        )
        .first()
    )

    if category is None:
        raise ValueError("Category not found")

    existing_product = (
        product_repository.get_product_by_name(
            db=db,
            product_name=product_data.product_name,
        )
    )

    if existing_product is not None:
        raise ValueError("Product name already exists")

    product = Product(
        ProductName=product_data.product_name,
        Description=product_data.description,
        CategoryID=product_data.category_id,
        Price=product_data.price,
        AvailableQuantity=product_data.available_quantity,
        ProductUrl=(
            str(product_data.product_url)
            if product_data.product_url is not None
            else None
        ),
    )

    return product_repository.create_product(
        db=db,
        product=product,
    )


def get_product_by_id(
    db: Session,
    product_id: int,
) -> Product | None:
    return product_repository.get_product_by_id(
        db=db,
        product_id=product_id,
    )


def get_all_products(db: Session) -> list[Product]:
    return product_repository.get_all_products(db)


def search_products(
    db: Session,
    name: str | None = None,
    category_id: int | None = None,
) -> list[Product]:
    if category_id is not None:
        category = category_repository.get_category_by_id(
            db=db,
            category_id=category_id,
        )

        if category is None:
            raise ValueError("Category not found")

    products = product_repository.search_products(
        db=db,
        name=name,
        category_id=category_id,
    )

    has_product_name = bool(name and name.strip())

    if (
        has_product_name
        and category_id is not None
        and not products
    ):
        raise ValueError(
            "Product not found in the selected category",
        )

    return products