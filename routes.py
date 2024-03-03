from flask import request, jsonify, Blueprint
from . import app,db
from .models import User, Music, Playlist

# bp = Blueprint('routes', __name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = User.generate_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not User.verify_hash(data['password'], user.password):
        return jsonify({'message': 'Invalid username or password'})
    return jsonify({'message': 'Login successful'})


# Add more routes for music and playlist CRUD operations
