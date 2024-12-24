# app.py
from flask import Flask
from app.routes.order_routes import order_routes
from app.routes.user_routes import user_routes

app = Flask(__name__)

# Register the API routes
app.register_blueprint(order_routes, url_prefix='/api')
app.register_blueprint(user_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
