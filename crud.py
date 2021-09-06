"""CRUD operations."""

from model import db, User, Track, Playlist, Playlist_Track, connect_to_db
from flask import session
from passlib.hash import argon2
import datetime

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


def create_track(title, artist, track_dur):
    """Creates a track."""
    # TODO check if track exists before creating

    track = Track(title = title, 
                  artist = artist,
                  track_dur = track_dur)
    
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


def create_user_playlist(tracks, user, playlist_name):
    """ Creates playlist saved by user """

    new_playlist = create_playlist(user, playlist_name)

    for track_name in tracks:
        create_playlist_track(new_playlist.playlist_id, get_track_id(track_name))
     
    return new_playlist

#########################################################

def get_user_by_email(email):
    """Look up user by email."""

    return User.query.filter(User.email == email).first()


def get_user_playlist(user):
    """ Displays user playlists """

    return Playlist.query.filter(Playlist.user_id == user).all()


def get_playlist_by_id(playlist_id):
    """ Returns a playlist by playlist id """

    return Playlist.query.filter(Playlist.playlist_id == playlist_id).first()


def get_track(track_id):
    """ Gets a track by track ID """

    return Track.query.get(track_id)


def get_track_id(title):
    """ Gets track ID by title of song """
   
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

def get_track_dur(track_id):
    """ Gets track duration by track ID """

    track_obj = Track.query.filter(Track.track_id == track_id).first()

    if track_obj:
        return str(track_obj.track_dur)        


def get_playlist_tracks(playlist_id):
    """ Gets list of all tracks in a user playlist """

    return Playlist_Track.query.filter(Playlist_Track.playlist_id == playlist_id).all()


def get_playlist_name(playlist_id):
    """ Gets playlist name by ID """

    playlist_obj = Playlist.query.filter(Playlist.playlist_id == playlist_id).first()

    if playlist_obj:
        return playlist_obj.name
    

def get_saved_playlists(user):
    """ Gets all saved user playlists """

    user_playlist_objs = Playlist.query.filter(Playlist.user_id == user).all()
   
    playlist_names = []

    if user_playlist_objs:
        for up_object in user_playlist_objs:
            playlist_names.append(up_object.name)

    return playlist_names


def get_user_playlist_ids(user):
    """ Gets playlists IDs under user """
    
    user_playlist_objs = Playlist.query.filter(Playlist.user_id == user).all()
    
    playlist_ids = []
    
    for up_object in user_playlist_objs:
        playlist_ids.append(up_object.playlist_id)
    
    return playlist_ids


def convert_millis(track_dur_lst):
    converted_track_times = []
    for track_dur in track_dur_lst:
        seconds = (int(track_dur)/1000)%60
        minutes = int(int(track_dur)/60000)
        hours = int(int(track_dur)/(60000*60))
        converted_time = '%02d:%02d:%02d' % (hours, minutes, seconds)
        converted_track_times.append(converted_time)
            
    return converted_track_times

if __name__ == '__main__':
    from server import app
    connect_to_db(app) 