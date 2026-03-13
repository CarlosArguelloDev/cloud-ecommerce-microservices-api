from app import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = "orders"

    id         = db.Column(db.Integer,    primary_key=True)
    user_id    = db.Column(db.Integer,    nullable=False)
    status     = db.Column(db.String(40), nullable=False, default="pending")
    # status: pending | confirmed | shipped | delivered | cancelled
    total      = db.Column(db.Float,      nullable=False, default=0.0)
    created_at = db.Column(db.DateTime,   default=datetime.utcnow)

    items      = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id":         self.id,
            "user_id":    self.user_id,
            "status":     self.status,
            "total":      self.total,
            "created_at": self.created_at.isoformat(),
            "items":      [item.to_dict() for item in self.items],
        }


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity   = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float,   nullable=False)

    def to_dict(self):
        return {
            "id":         self.id,
            "order_id":   self.order_id,
            "product_id": self.product_id,
            "quantity":   self.quantity,
            "unit_price": self.unit_price,
            "subtotal":   self.quantity * self.unit_price,
        }
