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



def get_track(track_id):
    """ Pulls a track """

    return Track.query.get(track_id)



# def add_playlist_to_user(playlist, user): 
#     """ Adds playlist """

#     user.playlists.append(playlist)

#     db.session.commit()


def get_playlist_by_id(playlist_id):
    """ Returns a playlist by playlist id """

    return Playlist.query.filter(Playlist.playlist_id == playlist_id).first()


# def add_track_to_playlist(playlist_id, track_id):
#     """ Add track to playlist """
    
#     pl = get_playlist_by_id(playlist_id)
#     pl.append(track_id)

    # db.session.commit()

def get_track_id(title):
    """ Gets track_id by title of song """
    # prob need to also include artist here bc dupe titles
    return Track.query.filter(Track.title == title).first()


def get_playlist_tracks(playlist_id):
    """ Gets list of all tracks in a user playlist """

    return Playlist_Track.query.filter(Playlist_Track.playlist_id == playlist_id).all()

##########################################################

def create_user_playlist(track_info):
    """ Creates playlist saved by user """

    #add a track to a playlist -- need to create this function
    #add to association table 
    #get paylist id and trackid just made and add to association table
    # user = get_user_by_email(session['EMAIL'])
    user = get_user_by_email('pollo@cat.com')
    new_playlist = create_playlist(user, 'Fresh New Playlist')

    for song in track_info.values():
        
        print(song[0])
        print(song[1])
        # track_id2 = get_track_id(track[1])
        # create_playlist_track(playlist_id, track_id)
        # create_playlist_track('4', track_id1)
        # # create_playlist_track('4', track_id2)
       
            


if __name__ == '__main__':
    from server import app
    connect_to_db(app) 