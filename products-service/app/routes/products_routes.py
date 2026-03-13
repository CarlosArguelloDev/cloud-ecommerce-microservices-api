from flask import Blueprint, jsonify
from app.controllers.products_controller import get_all_products, get_product_by_id

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def list_products():
    products = get_all_products()
    return jsonify(products), 200


@products_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


@products_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "products-service"}), 200
