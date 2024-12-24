from flask import Blueprint, request, jsonify
from app.services.portfolio_service import PortfolioService
from app.services.stock_service import StockService
from app.models import db, User, Portfolio, Stock
from app.exceptions import NotFoundException, BadRequestException

portfolio_controller = Blueprint('portfolio_controller', __name__)
portfolio_service = PortfolioService()
stock_service = StockService()

# Route to Get Portfolio (GET /api/portfolio/<user_id>)
@portfolio_controller.route('/<int:user_id>', methods=['GET'])
def get_portfolio(user_id):
    try:
        # Get user details
        user = User.query.get(user_id)
        if not user:
            raise NotFoundException(f'User with ID {user_id} not found.')

        # Get the portfolio for the user
        portfolio = portfolio_service.get_portfolio(user)
        
        return jsonify({
            'user_id': user.id,
            'stocks': [stock.to_dict() for stock in portfolio.stocks]
        }), 200

    except NotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# Route to Add Stock to Portfolio (POST /api/portfolio/add)
@portfolio_controller.route('/add', methods=['POST'])
def add_stock_to_portfolio():
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

        # Add stock to user's portfolio
        portfolio = portfolio_service.add_stock_to_portfolio(user, stock, quantity)

        return jsonify({'message': 'Stock added to portfolio successfully!', 'portfolio': portfolio.to_dict()}), 200

    except BadRequestException as e:
        return jsonify({'error': str(e)}), 400
    except NotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# Route to Remove Stock from Portfolio (POST /api/portfolio/remove)
@portfolio_controller.route('/remove', methods=['POST'])
def remove_stock_from_portfolio():
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

        # Remove stock from user's portfolio
        portfolio = portfolio_service.remove_stock_from_portfolio(user, stock, quantity)

        return jsonify({'message': 'Stock removed from portfolio successfully!', 'portfolio': portfolio.to_dict()}), 200

    except BadRequestException as e:
        return jsonify({'error': str(e)}), 400
    except NotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500
