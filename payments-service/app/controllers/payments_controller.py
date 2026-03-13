import uuid
import random
from app import db
from app.models.payment_model import Payment


def process_payment(data: dict):
    """
    data = {"order_id": int, "amount": float, "method": str}
    Simulates payment processing: 90% approval rate.
    """
    # Simulate processing: 90% success rate
    approved = random.random() < 0.90
    status    = "approved" if approved else "rejected"
    reference = f"LDV-{uuid.uuid4().hex[:10].upper()}" if approved else None

    payment = Payment(
        order_id=data["order_id"],
        amount=data["amount"],
        method=data.get("method", "card"),
        status=status,
        reference=reference,
    )
    db.session.add(payment)
    db.session.commit()
    return payment.to_dict()


def get_payment(payment_id: int):
    payment = Payment.query.get(payment_id)
    return payment.to_dict() if payment else None


def get_payments_by_order(order_id: int):
    payments = Payment.query.filter_by(order_id=order_id).all()
    return [p.to_dict() for p in payments]
