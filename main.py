from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LoginDemo.db'

db = SQLAlchemy(app)

## Define a Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def do_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active
        }
    
# Initialize the database
with app.app_context():
    db.create_all()


# Configure the HTTP routes CRUD (Create, Read, Update, Delete)
# GET method to retrieve the home page
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Login Demo API'})

# GET method to retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.do_dict() for user in users])

# GET method to retrieve a specific user by ID  
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.do_dict())
    else:
        return jsonify({'Error': 'User not found'}), 404

# POST method to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(key in data for key in ('email', 'password', 'first_name', 'last_name')):
        return jsonify({'Error': 'Missing required fields'}), 400
    
    new_user = User(
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        # Default to True till it is implemented a way to activate by email verification or something similar
        is_active=data.get('is_active', True)
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.do_dict()), 201

# PUT method to update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'Error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'Error': 'No data provided'}), 400
    
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify(user.do_dict())

# DELETE method to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'Error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 204

# POST Login user
@app.route('/users/login', methods=['POST'])
def login_user():
    data = request.get_json()
    print(data)
    if not data or not all(key in data for key in ('email', 'password')):
        return jsonify({'Error': 'Missing required fields'}), 400
    
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        return jsonify(user.do_dict())
    else:
        return jsonify({'Error': 'Invalid email or password'}), 401

if __name__ == '__main__':
    # To run and refresh all the time, add debug=True
    app.run(debug=True)
