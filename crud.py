"""CRUD operations."""

from model import db, User, Track, Playlist, Playlist_Track, connect_to_db
from flask import session
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
    # TODO check if track exists before creating

    track = Track(title = title, 
                artist = artist)
    
    db.session.add(track)
    db.session.commit()
    
    return track


def create_playlist_track(playlist_id, track_id):
    """ Creates a playlist track for a specific playlist """
    
    playlist_track = Playlist_Track(playlist_id = playlist_id, 
                                    track_id = track_id)

    db.session.add(playlist_track)
    db.session.commit()

    return playlist_track


def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(User.email == email).first()


def get_user_playlist(user):
    """ Displays user playlists """

    return Playlist.query.filter(Playlist.user_id == user).all()


def get_playlist_by_id(playlist_id):
    """ Returns a playlist by playlist id """

    return Playlist.query.filter(Playlist.playlist_id == playlist_id).first()


# If you have the track ID
def get_track(track_id):
    """ Pulls a track """

    return Track.query.get(track_id)


# Get ID by song title
def get_track_id(title):
    """ Gets track_id by title of song """
    # prob need to also include artist here bc dupe titles
    # this returns an object but I want it to return the 
    # just the track_id   object.track_id
    
    track_obj = Track.query.filter(Track.title == title).first()

    if track_obj:
        return str(track_obj.track_id)


def get_title_by_track_id(track_id):
    """ Gets track name by track ID """

    track_obj = Track.query.filter(Track.track_id == track_id).first()

    if track_obj:
        return str(track_obj.title)


def get_artist_by_track_id(track_id):
    """ Get artist name by track ID """

    artist_obj = Track.query.filter(Track.track_id == track_id).first()

    if artist_obj:
        return str(artist_obj.artist)


def get_playlist_tracks(playlist_id):
    """ Gets list of all tracks in a user playlist """

    return Playlist_Track.query.filter(Playlist_Track.playlist_id == playlist_id).all()


def create_user_playlist(artists, user, playlist_name):
    """ Creates playlist saved by user """

    new_playlist = create_playlist(user, playlist_name)

    for track_name in artists:
        create_playlist_track(new_playlist.playlist_id, get_track_id(track_name))
     
    return new_playlist
       
            
def get_playlist_name(playlist_id):
    """ Gets playlist name by ID """

    playlist_obj = Playlist.query.filter(Playlist.playlist_id == playlist_id).first()

    if playlist_obj:
        return playlist_obj.name


if __name__ == '__main__':
    from server import app
    connect_to_db(app) 