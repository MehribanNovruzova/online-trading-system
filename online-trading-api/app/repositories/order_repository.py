# app/repositories/order_repository.py
class OrderRepository:
    def __init__(self):
        self.orders = []  # Placeholder for actual database (replace with DB logic)

    def save(self, order):
        # Save the order to the database (or in-memory list)
        self.orders.append(order)
        return order

    def find_by_user_id(self, user_id):
        return [order for order in self.orders if order.user_id == user_id]
