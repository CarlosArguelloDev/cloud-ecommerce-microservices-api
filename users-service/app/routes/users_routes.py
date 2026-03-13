from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.users_controller import (
    register_user,
    login_user,
    get_user_by_id,
    get_wishlist,
    add_to_wishlist,
    remove_from_wishlist,
)

users_bp = Blueprint("users", __name__)


@users_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "users-service"}), 200


# ── Auth ──────────────────────────────────────────────────────────────────────

@users_bp.route("/users/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "email", "password")):
        return jsonify({"error": "name, email, and password are required"}), 400

    user, err = register_user(data)
    if err:
        return jsonify({"error": err}), 409
    return jsonify(user), 201


@users_bp.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "email and password are required"}), 400

    result, err = login_user(data)
    if err:
        return jsonify({"error": err}), 401
    return jsonify(result), 200


@users_bp.route("/users/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


# ── Wishlist ──────────────────────────────────────────────────────────────────

@users_bp.route("/users/wishlist", methods=["GET"])
@jwt_required()
def get_user_wishlist():
    user_id = int(get_jwt_identity())
    items = get_wishlist(user_id)
    return jsonify(items), 200


@users_bp.route("/users/wishlist", methods=["POST"])
@jwt_required()
def add_wishlist():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data or "product_id" not in data:
        return jsonify({"error": "product_id is required"}), 400

    item, err = add_to_wishlist(user_id, data["product_id"])
    if err == "Already in wishlist":
        return jsonify({"message": err, "item": item}), 200
    return jsonify(item), 201


@users_bp.route("/users/wishlist/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_wishlist(product_id):
    user_id = int(get_jwt_identity())
    removed = remove_from_wishlist(user_id, product_id)
    if not removed:
        return jsonify({"error": "Item not found in wishlist"}), 404
    return jsonify({"message": "Removed from wishlist"}), 200
