from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from passlib.hash import pbkdf2_sha256 as sha256
from flask import request, jsonify
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/music-app-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class Music(db.Model):
    __tablename__ = "musics"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    image = db.Column(LargeBinary, nullable=True)
    mp3_file = db.Column(LargeBinary, nullable=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('musics', lazy=True))

class Playlist(db.Model):
    __tablename__ = "playlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('playlists', lazy=True))

with app.app_context():
    db.create_all()

# Auth endpoints
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
    return jsonify({'id':user.id,'username':user.username,'message': 'Login successful'})


# User endpoints
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        user.username = data['username']
        db.session.commit()
        return jsonify({'message': 'User updated!'})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted!'})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/user/<int:user_id>/music', methods=['GET'])
def get_user_music(user_id):
    # data = request.json
    # user_id = data.get('user_id')

    # if not user_id:
    #     return jsonify({'message': 'User ID is required in the request body'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_music = Music.query.filter_by(user_id=user_id).all()
    if not user_music:
        return jsonify({'message': 'No music found for this user'}), 404
    print(user_music)
    music_list = []
    for music in user_music:
        music_data = {
            'title': music.title,
            'artist': music.artist,
            'image': base64.b64encode(music.image).decode('utf-8') if music.image else None,
            'mp3_file': base64.b64encode(music.mp3_file).decode('utf-8') if music.mp3_file else None
        }
        music_list.append(music_data)

    return jsonify({'music': music_list}), 200

# Music endpoints
@app.route('/music', methods=['POST'])
def create_music():
    data = request.form
    user_id = data.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    new_music = Music(
        title=data['title'],
        artist=data['artist'],
        image=request.files['image'].read() if 'image' in request.files else None,
        mp3_file=request.files['mp3_file'].read() if 'mp3_file' in request.files else None,
        user_id=user.id
    )

    db.session.add(new_music)
    db.session.commit()
    
    return jsonify({'message': 'New music created!'})


# Playlist endpoints
@app.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.get_json()
    new_playlist = Playlist(name=data['name'], user_id=data['user_id'])
    db.session.add(new_playlist)
    db.session.commit()
    return jsonify({'message': 'New playlist created!'})

@app.route('/playlists', methods=['GET'])
def get_all_playlists():
    playlists = Playlist.query.all()
    result = [{'id': playlist.id, 'name': playlist.name, 'user_id': playlist.user_id} for playlist in playlists]
    return jsonify(result)
