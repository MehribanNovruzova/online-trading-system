# app/routes/order_routes.py
from flask import Blueprint
from app.controllers.order_controller import OrderController

order_routes = Blueprint('order_routes', __name__)

order_controller = OrderController()

order_routes.route('/orders', methods=['POST'])(order_controller.create_order)
order_routes.route('/orders/<user_id>', methods=['GET'])(order_controller.get_orders)
