import bcrypt
from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer,     primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(200), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)  # bcrypt hash
    created_at = db.Column(db.DateTime,    default=datetime.utcnow)

    wishlist   = db.relationship("Wishlist", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, raw_password: str):
        self.password = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())

    def to_dict(self):
        return {
            "id":         self.id,
            "name":       self.name,
            "email":      self.email,
            "created_at": self.created_at.isoformat(),
        }


class Wishlist(db.Model):
    __tablename__ = "wishlists"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    added_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "user_id":    self.user_id,
            "product_id": self.product_id,
            "added_at":   self.added_at.isoformat(),
        }
