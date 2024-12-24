from app import db
from app.models.portfolio import Portfolio
from app.models.stock import Stock
from app.models.portfolio_stock import portfolio_stock
from app.models.transaction import Transaction
from app.services.stock_service import StockService

class PortfolioService:

    @staticmethod
    def create_portfolio(user_id, name):
        """
        Create a new portfolio for a specific user.
        """
        # Check if the portfolio with the given name already exists for the user
        if Portfolio.query.filter_by(user_id=user_id, name=name).first():
            return None

        # Create a new portfolio
        portfolio = Portfolio(user_id=user_id, name=name)
        db.session.add(portfolio)
        db.session.commit()

        return portfolio

    @staticmethod
    def get_portfolio_by_id(portfolio_id):
        """
        Retrieve a portfolio by its ID.
        """
        return Portfolio.query.get(portfolio_id)

    @staticmethod
    def get_portfolio_by_user_id(user_id):
        """
        Retrieve all portfolios belonging to a specific user.
        """
        return Portfolio.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_portfolio(portfolio_id, name=None):
        """
        Update the details of an existing portfolio.
        """
        portfolio = Portfolio.query.get(portfolio_id)
        if not portfolio:
            return None

        if name:
            portfolio.name = name

        db.session.commit()
        return portfolio

    @staticmethod
    def delete_portfolio(portfolio_id):
        """
        Delete a portfolio and all associated stocks.
        """
        portfolio = Portfolio.query.get(portfolio_id)
        if portfolio:
            # Remove all portfolio_stock associations before deleting the portfolio
            db.session.query(portfolio_stock).filter_by(portfolio_id=portfolio_id).delete()
            db.session.delete(portfolio)
            db.session.commit()
            return True
        return False

    @staticmethod
    def add_stock_to_portfolio(portfolio_id, stock_id, quantity):
        """
        Add a stock to a portfolio, creating a new portfolio_stock association.
        """
        portfolio = Portfolio.query.get(portfolio_id)
        stock = Stock.query.get(stock_id)

        if not portfolio or not stock:
            return None

        # Check if the stock already exists in the portfolio
        existing_stock = db.session.query(portfolio_stock).filter_by(portfolio_id=portfolio.id, stock_id=stock.id).first()
        if existing_stock:
            # If stock exists, update the quantity
            existing_stock.quantity += quantity
        else:
            # If stock doesn't exist in portfolio, create a new association
            new_stock = portfolio_stock(portfolio_id=portfolio.id, stock_id=stock.id, quantity=quantity)
            db.session.add(new_stock)

        db.session.commit()
        return True

    @staticmethod
    def remove_stock_from_portfolio(portfolio_id, stock_id, quantity):
        """
        Remove a specific quantity of a stock from a portfolio.
        """
        portfolio = Portfolio.query.get(portfolio_id)
        stock = Stock.query.get(stock_id)

        if not portfolio or not stock:
            return None

        # Find the existing stock entry in the portfolio
        existing_stock = db.session.query(portfolio_stock).filter_by(portfolio_id=portfolio.id, stock_id=stock.id).first()

        if not existing_stock or existing_stock.quantity < quantity:
            # If stock does not exist or quantity is not enough, return False
            return False

        # Decrease the quantity or delete the stock if quantity becomes zero
        existing_stock.quantity -= quantity
        if existing_stock.quantity == 0:
            db.session.delete(existing_stock)

        db.session.commit()
        return True

    @staticmethod
    def get_stocks_in_portfolio(portfolio_id):
        """
        Retrieve all stocks in a specific portfolio.
        """
        portfolio = Portfolio.query.get(portfolio_id)
        if not portfolio:
            return None

        # Retrieve all stocks and their quantities in the portfolio
        stocks = db.session.query(Stock, portfolio_stock.quantity).join(portfolio_stock).filter(portfolio_stock.portfolio_id == portfolio.id).all()
        return [{"stock": stock[0].to_dict(), "quantity": stock[1]} for stock in stocks]

    @staticmethod
    def get_all_portfolios():
        """
        Retrieve all portfolios in the system.
        """
        return Portfolio.query.all()
