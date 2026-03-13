from flask_jwt_extended import create_access_token
from app import db
from app.models.user_model import User, Wishlist


# ── Auth ──────────────────────────────────────────────────────────────────────

def register_user(data: dict):
    if User.query.filter_by(email=data["email"]).first():
        return None, "Email already registered"

    user = User(name=data["name"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), None


def login_user(data: dict):
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return None, "Invalid credentials"

    token = create_access_token(identity=str(user.id))
    return {"access_token": token, "user": user.to_dict()}, None


def get_user_by_id(user_id: int):
    user = User.query.get(user_id)
    return user.to_dict() if user else None


# ── Wishlist ──────────────────────────────────────────────────────────────────

def get_wishlist(user_id: int):
    items = Wishlist.query.filter_by(user_id=user_id).all()
    return [item.to_dict() for item in items]


def add_to_wishlist(user_id: int, product_id: int):
    existing = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        return existing.to_dict(), "Already in wishlist"

    item = Wishlist(user_id=user_id, product_id=product_id)
    db.session.add(item)
    db.session.commit()
    return item.to_dict(), None


def remove_from_wishlist(user_id: int, product_id: int):
    item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not item:
        return False
    db.session.delete(item)
    db.session.commit()
    return True
