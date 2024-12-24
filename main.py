# main.py
from app import create_app

# Entry point for the application
if __name__ == "__main__":
    # Create the Flask app using the factory function
    app = create_app()
    
    # Run the application (debug mode is typically used in development)
    app.run(debug=True, host='0.0.0.0', port=5000)
