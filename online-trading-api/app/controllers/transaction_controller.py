from flask import Blueprint, request, jsonify
from app.services.transaction_service import TransactionService
from app.services.stock_service import StockService
from app.models import db, User, Portfolio, Stock
from app.exceptions import NotFoundException, BadRequestException

transaction_controller = Blueprint('transaction_controller', __name__)
transaction_service = TransactionService()
stock_service = StockService()

# Route to Buy Stock (POST /api/transactions/buy)
@transaction_controller.route('/buy', methods=['POST'])
def buy_stock():
    try:
        # Get data from the request body
        user_id = request.json.get('user_id')
        stock_symbol = request.json.get('stock_symbol')
        quantity = request.json.get('quantity')

        # Validate input data
        if not user_id or not stock_symbol or not quantity:
            raise BadRequestException('user_id, stock_symbol, and quantity are required.')

        # Get the stock details
        stock = stock_service.get_stock_by_symbol(stock_symbol)
        if not stock:
            raise NotFoundException(f'Stock {stock_symbol} not found.')

        # Get user details
        user = User.query.get(user_id)
        if not user:
            raise NotFoundException(f'User with ID {user_id} not found.')

        # Perform the stock purchase (buying logic)
        transaction = transaction_service.buy_stock(user, stock, quantity)

        return jsonify({'message': 'Stock purchased successfully!', 'transaction': transaction.to_dict()}), 200

    except BadRequestException as e:
        return jsonify({'error': str(e)}), 400
    except NotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# Route to Sell Stock (POST /api/transactions/sell)
@transaction_controller.route('/sell', methods=['POST'])
def sell_stock():
    try:
        # Get data from the request body
        user_id = request.json.get('user_id')
        stock_symbol = request.json.get('stock_symbol')
        quantity = request.json.get('quantity')

        # Validate input data
        if not user_id or not stock_symbol or not quantity:
            raise BadRequestException('user_id, stock_symbol, and quantity are required.')

        # Get the stock details
        stock = stock_service.get_stock_by_symbol(stock_symbol)
        if not stock:
            raise NotFoundException(f'Stock {stock_symbol} not found.')

        # Get user details
        user = User.query.get(user_id)
        if not user:
            raise NotFoundException(f'User with ID {user_id} not found.')

        # Perform the stock sale (selling logic)
        transaction = transaction_service.sell_stock(user, stock, quantity)

        return jsonify({'message': 'Stock sold successfully!', 'transaction': transaction.to_dict()}), 200

    except BadRequestException as e:
        return jsonify({'error': str(e)}), 400
    except NotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# Route to Get Transaction History (GET /api/transactions/history/<user_id>)
@transaction_controller.route('/history/<int:user_id>', methods=['GET'])
def get_transaction_history(user_id):
    try:
        # Get user details
        user = User.query.get(user_id)
        if not user:
            raise NotFoundException(f'User with ID {user_id} not found.')

        # Get transaction history for the user
        transactions = transaction_service.get_transaction_history(user)

        return jsonify({'transactions': [t.to_dict() for t in transactions]}), 200

    except NotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500
