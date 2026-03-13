from app import db
from app.models.order_model import Order, OrderItem


def create_order(data: dict):
    """
    data = {
        "user_id": int,
        "items": [{"product_id": int, "quantity": int, "unit_price": float}]
    }
    """
    items_data = data.get("items", [])
    if not items_data:
        return None, "Order must contain at least one item"

    total = sum(i["unit_price"] * i["quantity"] for i in items_data)

    order = Order(user_id=data["user_id"], total=total, status="pending")
    db.session.add(order)
    db.session.flush()  # get order.id before commit

    for item in items_data:
        db.session.add(OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
        ))

    db.session.commit()
    return order.to_dict(), None


def get_order(order_id: int):
    order = Order.query.get(order_id)
    return order.to_dict() if order else None


def get_orders_by_user(user_id: int):
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return [o.to_dict() for o in orders]


def update_order_status(order_id: int, status: str):
    order = Order.query.get(order_id)
    if not order:
        return None
    order.status = status
    db.session.commit()
    return order.to_dict()
