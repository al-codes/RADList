""" Functions for calling Last FM API endpoints """

from server import *
import requests, os
import helper


LASTFM_API_KEY = os.environ['LASTFM_KEY']


def get_similar_artists(form_artist):
    """ Gets similar artists from Last FM API """

    # LAST FM endpoint for getting similar artists - API Call #1
    url1 = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar'

    payload = {'artist': form_artist,
                'api_key': LASTFM_API_KEY,
                'format': 'json',
                'limit' : 15}

    response = requests.get(url1, params=payload)
    data = response.json()

    similar_artists_list = []
    for i in range (15):
        similar_artists = (data['similarartists']['artist'][i])['name']
        similar_artists_list.append(similar_artists)
        similar_artists_list.append(similar_artists)

    return similar_artists_list


def get_top_tracks(sa_list):
    """ Gets top 2 tracks of each similar artist from LastFM API """
    
    top_track_list = []
    # LAST FM endpoint for getting artist's Top Tracks - API Call #2
    url2 = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks'

    # Loops through the similar artists list and inserts into payload
    for artist in sa_list[::2]:
        
        payload2 = {'artist': artist,
                    'api_key': LASTFM_API_KEY,
                    'format': 'json',
                    'limit': 2}
    
        response2 = requests.get(url2, params=payload2)
        artist_data = response2.json() 
        
        # Get Top 2 Tracks
        track_name_1 = artist_data['toptracks']['track'][0]['name']
        track_name_2 = artist_data['toptracks']['track'][1]['name']
        top_track_list.append(track_name_1)
        top_track_list.append(track_name_2)

    return top_track_list


def get_track_durations(sim_artists_and_top_tracks_dict):   

    track_duration_list = [] # milliseconds

    # LAST FM endpoint for getting artist's Top Tracks - API Call #3
    url3 = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo'

    for artist in sim_artists_and_top_tracks_dict.keys():
        for track in sim_artists_and_top_tracks_dict[artist]:

            payload3 = {'api_key': LASTFM_API_KEY,
                        'artist': artist,
                        'track': track,
                        'format': 'json'}

            response3 = requests.get(url3, params=payload3)
            track_dur_data = response3.json() 
           
            track_duration = track_dur_data['track']['duration']
            track_duration_list.append(track_duration)

    return track_duration_list



