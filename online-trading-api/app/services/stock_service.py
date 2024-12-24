from app import db
from app.models.stock import Stock

class StockService:

    @staticmethod
    def create_stock(name, symbol, price):
        """
        Create a new stock in the system.
        """
        # Check if the stock already exists by its symbol
        if Stock.query.filter_by(symbol=symbol).first():
            return None

        # Create a new stock
        stock = Stock(name=name, symbol=symbol, price=price)
        db.session.add(stock)
        db.session.commit()

        return stock

    @staticmethod
    def get_stock_by_id(stock_id):
        """
        Retrieve a stock by its ID.
        """
        return Stock.query.get(stock_id)

    @staticmethod
    def get_stock_by_symbol(symbol):
        """
        Retrieve a stock by its symbol (unique identifier for the stock).
        """
        return Stock.query.filter_by(symbol=symbol).first()

    @staticmethod
    def update_stock(stock_id, name=None, symbol=None, price=None):
        """
        Update the details of an existing stock.
        """
        stock = Stock.query.get(stock_id)
        if not stock:
            return None

        if name:
            stock.name = name
        if symbol:
            stock.symbol = symbol
        if price is not None:
            stock.price = price

        db.session.commit()
        return stock

    @staticmethod
    def delete_stock(stock_id):
        """
        Delete a stock from the system.
        """
        stock = Stock.query.get(stock_id)
        if stock:
            db.session.delete(stock)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_stocks():
        """
        Retrieve all stocks in the system.
        """
        return Stock.query.all()

    @staticmethod
    def update_stock_price(stock_id, new_price):
        """
        Update the price of an existing stock.
        """
        stock = Stock.query.get(stock_id)
        if stock:
            stock.price = new_price
            db.session.commit()
            return stock
        return None
