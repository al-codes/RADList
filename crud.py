"""CRUD operations."""

from model import db, User, Track, Playlist, Playlist_Track, connect_to_db
from passlib.hash import argon2


def create_user(fname, lname, email, password):
    """Creates a new user."""

    user = User(fname=fname, 
                lname=lname, 
                email=email, 
                password=argon2.hash(password), 
                )

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
    # to test, have to create user with variable name and then 
    # plug that user_var into this fcn


def create_track(title, artist):
    """Creates a track."""
    
    track = Track(title = title, 
                artist = artist)
    
    db.session.add(track)
    db.session.commit()
    
    return track



def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(User.email == email).first()


def get_user_playlist(user):
    """ Displays user playlists """

    return User.query.filter(User.playlists == user).all()



def get_track(track_id):
    """ Pulls a track """

    return Track.query.filter(Track.track_id == track_id).first()


def add_playlist_to_user(playlist, user): 
    """ Adds playlist """

    user.playlists.append(playlist)

    db.session.commit()



def get_playlist_by_id(playlist_id):
    """ Returns a playlist by playlist id """

    return Playlist.query.filter(Playlist.playlist_id == playlist_id).first()


def add_track_to_playlist(playlist_id, track_id):
    """ Add track to playlist """
    get_playlist_by_id(playlist_id)
    get_track(track_id)

pass

def create_user_playlist(playlist_dict):
    """ Creates playlist saved by user """
    #before for loop, call create playlist fcn
    #after creating tracks in loop
    #add a track to a playlist -- need to create this function
    #add to association table 
    #get paylist id and trackid just made and add to association table
    create_playlist(user, 'My Saved Playlist')

    for name, track in playlist_dict.items():
        create_track(track[0], name)
        create_track(track[1], name)


if __name__ == '__main__':
    from server import app
    connect_to_db(app) 