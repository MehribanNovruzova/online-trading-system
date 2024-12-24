# app/controllers/order_controller.py
from flask import jsonify, request
from app.services.order_service import OrderService

class OrderController:
    def __init__(self):
        self.order_service = OrderService()

    def create_order(self):
        data = request.get_json()
        user_id = data['user_id']
        stock_symbol = data['stock_symbol']
        quantity = data['quantity']
        price = data['price']
        order_type = data['order_type']

        try:
            order = self.order_service.create_order(user_id, stock_symbol, quantity, price, order_type)
            return jsonify(order.__dict__), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def get_orders(self, user_id):
        orders = self.order_service.get_orders(user_id)
        return jsonify([order.__dict__ for order in orders]), 200
