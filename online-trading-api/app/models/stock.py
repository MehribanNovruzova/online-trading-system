from app import db

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    market_cap = db.Column(db.Float, nullable=True)
    volume = db.Column(db.Integer, nullable=True)
    
    # Defining the relationship with transactions (if any)
    # transactions = db.relationship('Transaction', backref='stock', lazy=True)

    def __repr__(self):
        return f'<Stock {self.name} ({self.symbol})>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'current_price': self.current_price,
            'market_cap': self.market_cap,
            'volume': self.volume
        }
