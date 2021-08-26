"""CRUD operations."""

from model import (db, User, Track, Playlist, Playlist_Track, connect_to_db)
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
    # plug that user var into this fcn

def create_track(title, artist):
    """Creates a track."""
    
    track = Track(title = title, 
                  artist = artist)
    
    db.session.add(track)
    db.session.commit()
    
    return track

def add_playlist_to_user(playlist, user):
    """ Adds playlist """

    user.playlists.append(playlist)

    db.session.commit()


def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(User.email == email).first()

def get_user_playlist(user):
    """ Displays user playlists """

    return User.query.filter(User.playlists == user).all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app) 