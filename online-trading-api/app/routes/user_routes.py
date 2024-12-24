from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.services.portfolio_service import PortfolioService

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/', methods=['POST'])
def create_user():
    """
    Create a new user.
    The request body must contain 'username', 'email', and 'password'.
    """
    data = request.get_json()

    if not data or not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({"message": "Missing required fields"}), 400

    user = UserService.create_user(data['username'], data['email'], data['password'])

    return jsonify(user.to_dict()), 201

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a specific user by their user_id.
    """
    user = UserService.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404

@bp.route('/<int:user_id>/portfolio', methods=['GET'])
def get_user_portfolio(user_id):
    """
    Get the user's portfolio.
    """
    portfolio = PortfolioService.get_portfolio_by_user(user_id)
    if portfolio:
        return jsonify(portfolio.to_dict()), 200
    return jsonify({"message": "Portfolio not found"}), 404

@bp.route('/<int:user_id>/portfolio', methods=['POST'])
def create_user_portfolio(user_id):
    """
    Create a portfolio for the user.
    """
    portfolio = PortfolioService.create_portfolio(user_id)
    return jsonify(portfolio.to_dict()), 201

@bp.route('/login', methods=['POST'])
def login_user():
    """
    User login. The request body must contain 'email' and 'password'.
    """
    data = request.get_json()

    if not data or not all(key in data for key in ['email', 'password']):
        return jsonify({"message": "Missing required fields"}), 400

    user = UserService.authenticate_user(data['email'], data['password'])
    if user:
        # Generate a token (if using JWT or other token-based auth) or set a session here.
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/<int:user_id>/portfolio/value', methods=['GET'])
def get_portfolio_value(user_id):
    """
    Get the value of the user's portfolio.
    """
    portfolio = PortfolioService.get_portfolio_by_user(user_id)
    if portfolio:
        value = PortfolioService.calculate_portfolio_value(portfolio.id)
        return jsonify({"portfolio_value": value}), 200
    return jsonify({"message": "Portfolio not found"}), 404
