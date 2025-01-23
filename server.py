from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import bcrypt

# Initialize Flask app
app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres.qanmiazixizmcjawwvlk",
    "password": "Flaa1D9xs76i6cjY",
    "host": "aws-0-ap-south-1.pooler.supabase.com",
    "port": 5432
}

# SQLAlchemy database URI setup
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary track modifications

# Initialize CORS
CORS(app)

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize migrations

# User Model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def to_dict(self):
        """Manually serialize User object to dictionary"""
        return {"id": self.id, "email": self.email, "created_at": self.created_at}

# Root Route
@app.route('/')
def root():
    return 'Server is running!'

# Store user credentials (Hash password and save to DB)
@app.route('/store-credentials', methods=['POST'])
def store_credentials():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            'error': 'Email and password are required',
            'shouldNavigate': False
        }), 400

    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': f'User with email {email} already exists'}), 400

        # Create a new user
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'User stored successfully',
            'user': user.to_dict(),  # Manually serialize the user
            'shouldNavigate': True,
            'navigateTo': '/verification'  # or wherever you want to navigate
        }), 200

    except Exception as err:
        return jsonify({
            'success': False,
            'error': 'Error saving credentials',
            'details': str(err),
            'shouldNavigate': False
        }), 500

# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])  # Manually serialize each user

# Get a user by ID
@app.route("/user/<int:id>", methods=["GET"])
def get_user_by_id(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error": f"User with id {id} not found"}), 400

    return jsonify(user.to_dict())  # Manually serialize the user

if __name__ == '__main__':
    app.run(debug=True)
