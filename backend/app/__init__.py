from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary, Table, Column, Integer, ForeignKey
from passlib.hash import pbkdf2_sha256 as sha256
from flask import request, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)
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

association_table = Table('association', db.Model.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('music_id', Integer, ForeignKey('musics.id'))
)

class Music(db.Model):
    __tablename__ = "musics"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    image = db.Column(LargeBinary, nullable=True)
    mp3_file = db.Column(LargeBinary, nullable=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('musics', lazy=True))
    like = db.Column(db.Boolean,nullable=True)
    playlists = db.relationship('Playlist', secondary=association_table, back_populates='musics')

class Playlist(db.Model):
    __tablename__ = "playlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(LargeBinary, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('playlists', lazy=True))
    musics = db.relationship('Music', secondary=association_table, back_populates='playlists')

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
            'id':music.id,
            'title': music.title,
            'artist': music.artist,
            'image': base64.b64encode(music.image).decode('utf-8') if music.image else None,
            'mp3_file': base64.b64encode(music.mp3_file).decode('utf-8') if music.mp3_file else None,
            'like':music.like
        }
        music_list.append(music_data)

    return jsonify({'music': music_list}), 200

@app.route('/user/<int:user_id>/favorits', methods=['GET'])
def get_user_music_favorits(user_id):

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_music = Music.query.filter_by(user_id=user_id).all()
    if not user_music:
        return jsonify({'message': 'No music found for this user'}), 404
    print(user_music)
    music_list = []
    for music in user_music:
        if music.like:
            music_data = {
                'id':music.id,
                'title': music.title,
                'artist': music.artist,
                'image': base64.b64encode(music.image).decode('utf-8') if music.image else None,
                'mp3_file': base64.b64encode(music.mp3_file).decode('utf-8') if music.mp3_file else None,
                'like':music.like
            }

            music_list.append(music_data)

    return jsonify({'music': music_list}), 200

@app.route('/user/<int:user_id>/playlists', methods=['GET'])
def get_user_playlist(user_id):

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_playlists = Playlist.query.filter_by(user_id=user_id).all()
    if not user_playlists:
        return jsonify({'message': 'No music found for this user'}), 404
    print(user_playlists)
    playlists = []
    for playlist in user_playlists:
        playlist_data = {
            'id':playlist.id,
            'name': playlist.name,
            'image': base64.b64encode(playlist.image).decode('utf-8') if playlist.image else None,
        }
        playlists.append(playlist_data)

    return jsonify({'data': playlists}), 200

# Music endpoints
@app.route('/music', methods=['POST'])
def create_music():
    data = request.form
    print(data)
    user_id = data.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    new_music = Music(
        title=data['title'],
        artist=data['artist'],
        image=request.files['image'].read() if 'image' in request.files else None,
        mp3_file=request.files['mp3_file'].read() if 'mp3_file' in request.files else None,
        user_id=user.id,
        like=False
    )

    db.session.add(new_music)
    db.session.commit()
    
    return jsonify({'message': 'New music created!'})

@app.route('/music/<int:music_id>/add_fav', methods=['POST'])
def add_to_fav(music_id):
    music = Music.query.get(music_id)

    music.like = True
    
    db.session.commit()
    
    return jsonify({'message': 'Music added to favorits successfully'})

@app.route('/music/<int:music_id>/remove_fav', methods=['POST'])
def remove_from_fav(music_id):
    music = Music.query.get(music_id)

    music.like = False
    
    db.session.commit()
    
    return jsonify({'message': 'Music removed from favorits successfully'})

# Playlist endpoints
@app.route('/playlist', methods=['POST'])
def create_playlist():
    data = request.form
    new_playlist = Playlist(
        name=data['name'], 
        user_id=data['user_id'], 
        image=request.files['image'].read() if 'image' in request.files else None
    )
    db.session.add(new_playlist)
    db.session.commit()
    return jsonify({'message': 'New playlist created!'})

@app.route('/playlist/<int:playlist_id>/add_music', methods=['POST'])
def add_music_to_playlist(playlist_id):
    # Assuming the request contains JSON data with music_id
    request_data = request.get_json()

    music_id = request_data.get('music_id')
    if music_id is None:
        return jsonify({'error': 'No music_id provided'}), 400

    # Fetch the playlist and music objects from the database
    playlist = Playlist.query.get_or_404(playlist_id)
    music = Music.query.get_or_404(music_id)

    # Add the music to the playlist
    playlist.musics.append(music)
    
    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': f'Music added to playlist {playlist.name} successfully'}), 200

def get_music_by_playlist_id(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if playlist:
        return playlist.musics
    else:
        return []
    
@app.route('/playlist/<int:playlist_id>/music', methods=['GET'])
def get_music_by_playlist(playlist_id):
    music = get_music_by_playlist_id(playlist_id)
    if music:
        # Create a list of music data for the playlist
        music_list = [{
            'id':track.id,
            'title': track.title,
            'artist': track.artist,
            'image': base64.b64encode(track.image).decode('utf-8') if track.image else None,
            'mp3_file': base64.b64encode(track.mp3_file).decode('utf-8') if track.mp3_file else None,
            'like':track.like
            # Add more attributes as needed
        } for track in music]

        return jsonify(music_list), 200
    else:
        return jsonify({'error': 'Playlist not found'}), 404