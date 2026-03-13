from app import db
from datetime import datetime
import random


class Payment(db.Model):
    __tablename__ = "payments"

    id         = db.Column(db.Integer,    primary_key=True)
    order_id   = db.Column(db.Integer,    nullable=False)
    amount     = db.Column(db.Float,      nullable=False)
    method     = db.Column(db.String(40), nullable=False, default="card")
    # method: card | transfer | cash
    status     = db.Column(db.String(40), nullable=False, default="pending")
    # status: pending | approved | rejected
    reference  = db.Column(db.String(80), nullable=True)   # simulated transaction ID
    created_at = db.Column(db.DateTime,   default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "order_id":   self.order_id,
            "amount":     self.amount,
            "method":     self.method,
            "status":     self.status,
            "reference":  self.reference,
            "created_at": self.created_at.isoformat(),
        }
