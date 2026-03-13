from app.models.product_model import Product
from app import db


def get_all_products():
    products = Product.query.all()
    return [p.to_dict() for p in products]


def get_product_by_id(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        return None
    return product.to_dict()
