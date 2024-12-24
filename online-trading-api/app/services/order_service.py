# app/services/order_service.py
from app.repositories.order_repository import OrderRepository
from app.models.order import Order

class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()

    def create_order(self, data):
        order = Order(None, data["user_id"], data["stock_symbol"], data["quantity"], data["price"], data["order_type"])

        if order.calculate_total() > 100000:  # Business rule: limit order value
            raise ValueError("Order exceeds maximum allowed value")

        return self.order_repository.save(order)

    def get_orders(self, user_id):
        return self.order_repository.find_by_user_id(user_id)
