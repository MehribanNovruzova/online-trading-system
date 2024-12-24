from app import db
from app.models.transaction import Transaction
from app.models.stock import Stock
from app.models.portfolio_stock import portfolio_stock
from app.models.portfolio import Portfolio
from app.services.stock_service import StockService
from app.services.portfolio_service import PortfolioService

class TransactionService:

    @staticmethod
    def create_transaction(portfolio_id, stock_id, quantity, transaction_type, price_per_stock):
        """
        Create a new transaction (buy/sell) for a specific portfolio.
        transaction_type can be either 'buy' or 'sell'.
        """
        portfolio = Portfolio.query.get(portfolio_id)
        stock = Stock.query.get(stock_id)

        if not portfolio or not stock:
            return None

        # Validate stock quantity before making the transaction
        if transaction_type == 'buy':
            # Check if portfolio has enough funds or allow unlimited funds for simplicity
            pass
        elif transaction_type == 'sell':
            # Check if portfolio has enough stock quantity
            existing_stock = db.session.query(portfolio_stock).filter_by(portfolio_id=portfolio.id, stock_id=stock.id).first()
            if not existing_stock or existing_stock.quantity < quantity:
                return None

        # Create the transaction
        transaction = Transaction(
            portfolio_id=portfolio_id,
            stock_id=stock_id,
            quantity=quantity,
            transaction_type=transaction_type,
            price_per_stock=price_per_stock
        )

        # Update portfolio stock if it's a buy
        if transaction_type == 'buy':
            PortfolioService.add_stock_to_portfolio(portfolio_id, stock_id, quantity)
        elif transaction_type == 'sell':
            PortfolioService.remove_stock_from_portfolio(portfolio_id, stock_id, quantity)

        # Add transaction to the database
        db.session.add(transaction)
        db.session.commit()

        return transaction

    @staticmethod
    def get_transaction_by_id(transaction_id):
        """
        Retrieve a transaction by its ID.
        """
        return Transaction.query.get(transaction_id)

    @staticmethod
    def get_transactions_by_portfolio(portfolio_id):
        """
        Retrieve all transactions for a specific portfolio.
        """
        return Transaction.query.filter_by(portfolio_id=portfolio_id).all()

    @staticmethod
    def get_all_transactions():
        """
        Retrieve all transactions in the system.
        """
        return Transaction.query.all()
