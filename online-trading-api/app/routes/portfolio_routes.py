from flask import Blueprint, request, jsonify
from app.services.portfolio_service import PortfolioService
from app.services.stock_service import StockService
from app.services.transaction_service import TransactionService

bp = Blueprint('portfolio', __name__, url_prefix='/portfolios')

@bp.route('/', methods=['POST'])
def create_portfolio():
    """
    Create a new portfolio for a user.
    The request body must contain 'user_id'.
    """
    data = request.get_json()

    if not data or 'user_id' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    user_id = data['user_id']
    portfolio = PortfolioService.create_portfolio(user_id)

    if portfolio:
        return jsonify(portfolio.to_dict()), 201
    return jsonify({"message": "Failed to create portfolio"}), 400

@bp.route('/<int:portfolio_id>', methods=['GET'])
def get_portfolio(portfolio_id):
    """
    Get details of a specific portfolio by portfolio_id.
    """
    portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
    if portfolio:
        return jsonify(portfolio.to_dict()), 200
    return jsonify({"message": "Portfolio not found"}), 404

@bp.route('/<int:portfolio_id>/stocks', methods=['POST'])
def add_stock_to_portfolio(portfolio_id):
    """
    Add a stock to a specific portfolio.
    The request body must contain 'stock_id' and 'quantity'.
    """
    data = request.get_json()

    if not data or not all(key in data for key in ['stock_id', 'quantity']):
        return jsonify({"message": "Missing required fields"}), 400

    stock_id = data['stock_id']
    quantity = data['quantity']

    # Check if the stock exists
    stock = StockService.get_stock_by_id(stock_id)
    if not stock:
        return jsonify({"message": "Stock not found"}), 404

    portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
    if not portfolio:
        return jsonify({"message": "Portfolio not found"}), 404

    # Add stock to portfolio
    portfolio_stock = PortfolioService.add_stock_to_portfolio(portfolio_id, stock_id, quantity)
    if portfolio_stock:
        return jsonify(portfolio_stock.to_dict()), 200
    return jsonify({"message": "Failed to add stock to portfolio"}), 400

@bp.route('/<int:portfolio_id>/stocks', methods=['GET'])
def get_portfolio_stocks(portfolio_id):
    """
    Get all stocks in a specific portfolio.
    """
    portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
    if not portfolio:
        return jsonify({"message": "Portfolio not found"}), 404

    stocks = PortfolioService.get_stocks_in_portfolio(portfolio_id)
    return jsonify([stock.to_dict() for stock in stocks]), 200

@bp.route('/<int:portfolio_id>/value', methods=['GET'])
def get_portfolio_value(portfolio_id):
    """
    Get the total value of a portfolio based on its stocks.
    """
    portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
    if not portfolio:
        return jsonify({"message": "Portfolio not found"}), 404

    total_value = PortfolioService.calculate_portfolio_value(portfolio_id)
    return jsonify({"total_value": total_value}), 200

@bp.route('/<int:portfolio_id>/transactions', methods=['GET'])
def get_portfolio_transactions(portfolio_id):
    """
    Get all transactions for a specific portfolio.
    """
    transactions = TransactionService.get_transactions_by_portfolio(portfolio_id)
    if transactions:
        return jsonify([transaction.to_dict() for transaction in transactions]), 200
    return jsonify({"message": "No transactions found for this portfolio"}), 404
