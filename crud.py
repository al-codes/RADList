"""CRUD operations."""

from model import db, User, Track, Playlist, Playlist_Track, connect_to_db

def create_user(fname, lname, email, password):
    """Creates a new user."""

    user = User(fname = fname, 
                lname = lname, 
                email = email, 
                password = password)

    db.session.add(user)
    db.session.commit()

    return user

def create_playlist(user, name):
    """Creates a playlist."""

    playlist = Playlist(user = user, 
                        name = name)

    db.session.add(playlist)
    db.session.commit()

    return playlist

def create_track(title, artist):
    """Creates a track."""
    
    track = Track(title = title, 
                  artist = artist)
    
    db.session.add(track)
    db.session.commit()
    
    return track



if __name__ == '__main__':
    from server import app
    connect_to_db(app) #line 67 in connect to db -- name app not defined in app.config['SQLALCHEMY_DATABASE_URI'] = db_uri