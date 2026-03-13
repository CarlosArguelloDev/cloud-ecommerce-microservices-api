from flask import Blueprint, jsonify, request
from app.controllers.orders_controller import (
    create_order,
    get_order,
    get_orders_by_user,
    update_order_status,
)

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "orders-service"}), 200


@orders_bp.route("/orders", methods=["POST"])
def new_order():
    data = request.get_json()
    if not data or "user_id" not in data or "items" not in data:
        return jsonify({"error": "user_id and items are required"}), 400

    order, err = create_order(data)
    if err:
        return jsonify({"error": err}), 400
    return jsonify(order), 201


@orders_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_one_order(order_id):
    order = get_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200


@orders_bp.route("/orders/user/<int:user_id>", methods=["GET"])
def get_user_orders(user_id):
    orders = get_orders_by_user(user_id)
    return jsonify(orders), 200


@orders_bp.route("/orders/<int:order_id>/status", methods=["PUT"])
def set_order_status(order_id):
    data = request.get_json()
    if not data or "status" not in data:
        return jsonify({"error": "status is required"}), 400

    valid_statuses = {"pending", "confirmed", "shipped", "delivered", "cancelled"}
    if data["status"] not in valid_statuses:
        return jsonify({"error": f"status must be one of {valid_statuses}"}), 400

    order = update_order_status(order_id, data["status"])
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200
