from flask import Flask
from app.controllers.user_controller import user_controller
from app.controllers.stock_controller import stock_controller
from app.controllers.transaction_controller import transaction_controller
from app.controllers.portfolio_controller import portfolio_controller
from app.config import Config
from app.models import db

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize the database
    db.init_app(app)
    
    # Register Blueprints (Controllers)
    app.register_blueprint(user_controller, url_prefix='/api/users')
    app.register_blueprint(stock_controller, url_prefix='/api/stocks')
    app.register_blueprint(transaction_controller, url_prefix='/api/transactions')
    app.register_blueprint(portfolio_controller, url_prefix='/api/portfolio')
    
    return app

# Entry point to run the application
if __name__ == '__main__':
    app = create_app()
    
    # Create database tables (if not created yet)
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True)
