""" RAD List db tables """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from passlib.hash import argon2


db = SQLAlchemy()



class User(db.Model):
    """Data model for a user."""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    photo = db.Column(db.String) # nullable

    playlists = db.relationship("Playlist")
    

    def __repr__(self):
        return f'<User user_id={self.user_id}, Full name={self.fname} {self.lname}, email={self.email}>'

# class UserPlaylist(db.Model):

#     __tablename__ = "user_playlists"

#     user_playlist_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'), nullable=False)
    
#     users = db.relationship("User")

#     def __repr__(self):
#         return f'<UserPlaylist user_playlist_id={self.user_playlist_id} user_id={self.user_id}>'


class Playlist(db.Model):
    """Data model for a playlist."""

    __tablename__ = "playlists"
    
    playlist_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # user = db.relationship("User")
    user = db.relationship("User", overlaps="playlists") #relation between users and playlist defined here
    tracks = db.relationship("Track",
                             secondary="playlist_tracks",
                             backref="playlists") #added additional info here with secondary
                             
    def __repr__(self):
        return f'<Playlist playlist_id={self.playlist_id} name={self.name} user_id={self.user_id}>'


class Track(db.Model):
    """Data model for a track."""

    __tablename__ = "tracks"

    track_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    track_dur = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Track track_id={self.track_id} title={self.title} artist={self.artist} track_dur={self.track_dur}>'



class Playlist_Track(db.Model):
    """Data model for a playlist track assoc table."""
    
    __tablename__ = "playlist_tracks"

    playlist_track_id = db.Column(db.Integer, primary_key=True, nullable=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.track_id'), nullable=False)

    # playlist = db.relationship("Playlist", backref="playlist_tracks") # dont need bc relationship defined already
    # track = db.relationship("Track", backref="playlist_tracks")

    
    def __repr__(self):
        return f'<Playlist_Track playlist_id={self.playlist_id} track_id={self.track_id}>'


    
def connect_to_db(flask_app, db_uri='postgresql:///radlist', echo=False):
    """Connect the database to our Flask app."""

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

def create_fake_data():
    """ Create fake users for testing """

    User.query.delete()
    Track.query.delete()
    Playlist.query.delete()

    anne = User(fname='Anne', lname='Ortiz', email='anne@test.com', password=argon2.hash('anne'))
    nik = User(fname='Nik', lname='Alvarez', email='nik@test.com', password=argon2.hash('nik'))
    track_list = []
    
    track1 = Track(title='Common People', artist='Pulp', track_dur='00:03:58')
    track2 = Track(title='Coffee and TV', artist='Blur', track_dur='00:02:30')
    track_list.append(track1)
    track_list.append(track2)
    playlist = Playlist(user=nik, name='Test Playlist')
    db.session.add_all([anne, nik, track1, track2, playlist])
  
    db.session.commit()

    # # playlist_track1 = Playlist_Track(playlist_id=playlist.playlist_id, track_id=track1.track_id)
    # # playlist_track2 = Playlist_Track(playlist_id=playlist.playlist_id, track_id=track2.track_id)
    # db.session.add(playlist)
    # # db.session.add_all([playlist, playlist_track1, playlist_track2])    
    # db.session.commit()





if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    