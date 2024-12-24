# app/models/order.py
class Order:
    def __init__(self, id, user_id, stock_symbol, quantity, price, order_type):
        self.id = id
        self.user_id = user_id
        self.stock_symbol = stock_symbol
        self.quantity = quantity
        self.price = price
        self.order_type = order_type  # 'buy' or 'sell'

    def calculate_total(self):
        return self.quantity * self.price

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "stock_symbol": self.stock_symbol,
            "quantity": self.quantity,
            "price": self.price,
            "order_type": self.order_type,
            "total": self.calculate_total(),
        }
