from flask import Blueprint, request, jsonify
from app.services.stock_service import StockService

stock_controller = Blueprint('stock_controller', __name__)
stock_service = StockService()

@stock_controller.route('/stock/<symbol>', methods=['GET'])
def get_stock(symbol):
    stock_data = stock_service.get_stock_price(symbol)
    return jsonify(stock_data)

@stock_controller.route('/buy', methods=['POST'])
def buy_stock():
    user_id = request.json.get('user_id')
    symbol = request.json.get('symbol')
    quantity = request.json.get('quantity')
    
    # Logic to buy stock
    stock_service.buy_stock(user_id, symbol, quantity)
    return jsonify({'message': 'Stock purchased successfully'}), 200
