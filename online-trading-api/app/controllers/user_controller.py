from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from app.services.user_service import UserService
from app.exceptions import NotFoundException, BadRequestException

user_controller = Blueprint('user_controller', __name__)
user_service = UserService()

# User Registration Route (POST /api/users/register)
@user_controller.route('/register', methods=['POST'])
def register_user():
    try:
        # Get user data from the request
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        
        # Validate input data
        if not username or not email or not password:
            raise BadRequestException('Username, email, and password are required.')

        # Check if the user already exists
        if user_service.get_user_by_email(email):
            raise BadRequestException('Email is already in use.')
        
        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create the new user
        user = User(username=username, email=email, password_hash=hashed_password)
        
        # Save user to the database
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully!'}), 201

    except BadRequestException as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# User Login Route (POST /api/users/login)
@user_controller.route('/login', methods=['POST'])
def login_user():
    try:
        # Get login data from the request
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            raise BadRequestException('Email and password are required.')

        # Find user by email
        user = user_service.get_user_by_email(email)
        if not user:
            raise NotFoundException('User not found.')

        # Check if the password is correct
        if not check_password_hash(user.password_hash, password):
            raise BadRequestException('Invalid password.')

        # Create and return a JWT token (assuming JWT is used for authentication)
        token = user_service.generate_jwt(user)

        return jsonify({'message': 'Login successful', 'token': token}), 200

    except BadRequestException as e:
        return jsonify({'error': str(e)}), 400
    except NotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# Get User Details Route (GET /api/users/<user_id>)
@user_controller.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Fetch the user by user_id
        user = user_service.get_user_by_id(user_id)
        
        if not user:
            raise NotFoundException('User not found.')

        # Return user data
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }), 200

    except NotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500
