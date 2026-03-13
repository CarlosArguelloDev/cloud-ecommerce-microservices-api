from flask import Blueprint, jsonify, request
from app.controllers.payments_controller import (
    process_payment,
    get_payment,
    get_payments_by_order,
)

payments_bp = Blueprint("payments", __name__)


@payments_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "payments-service"}), 200


@payments_bp.route("/payments", methods=["POST"])
def new_payment():
    data = request.get_json()
    if not data or not all(k in data for k in ("order_id", "amount")):
        return jsonify({"error": "order_id and amount are required"}), 400

    payment = process_payment(data)
    status_code = 201 if payment["status"] == "approved" else 402
    return jsonify(payment), status_code


@payments_bp.route("/payments/<int:payment_id>", methods=["GET"])
def get_one_payment(payment_id):
    payment = get_payment(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(payment), 200


@payments_bp.route("/payments/order/<int:order_id>", methods=["GET"])
def get_order_payments(order_id):
    payments = get_payments_by_order(order_id)
    return jsonify(payments), 200
