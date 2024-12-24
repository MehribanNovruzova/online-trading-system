from app import db

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stocks = db.relationship('Stock', secondary='portfolio_stock', lazy='subquery', backref=db.backref('portfolios', lazy=True))
    # The above line defines a many-to-many relationship with Stock using the 'portfolio_stock' association table.

    def __repr__(self):
        return f'<Portfolio of User {self.user_id}>'

    def to_dict(self):
        # Returns a dictionary representation of the portfolio, with the user and stocks
        return {
            'id': self.id,
            'user_id': self.user_id,
            'stocks': [stock.to_dict() for stock in self.stocks]
        }
