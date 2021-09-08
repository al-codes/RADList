""" Server for RAD List """

from flask import Flask, render_template, redirect, request, session, flash, jsonify
from jinja2 import StrictUndefined
from model import connect_to_db, User, Playlist, Track
import requests, os
import crud, helper, lastfm_api
from passlib.hash import argon2
import json



app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True
LASTFM_API_KEY = os.environ['LASTFM_KEY']



@app.route('/')
def index():
    """ Display homepage """
    if session:
        return redirect ('/search')
    else:
        return render_template('homepage.html')


@app.route('/users/create-user.json', methods=['POST'])
def signup_user():
    """ Process user signup form """
    
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    user = crud.get_user_by_email(email)

    if user != None:
        return jsonify('This email is already taken.')

    else:
        crud.create_user(fname, lname, email, password)
        user = crud.get_user_by_email(email) 
        session['EMAIL'] = user.email
        session['FNAME'] = user.fname 
        session['LNAME'] = user.lname
        session['ID'] = user.user_id
        return jsonify('You have registered successfully. Please log in.')


@app.route('/login', methods=['POST'])
def process_login():
    """ Logs in a user """
  
    email = request.form.get('email')
    input_password = request.form.get('password')
    user = crud.get_user_by_email(email) 
   
    
    if user == None:
        flash('Email does not exist. Please sign up or try again.')
        return redirect('/')
    
    elif (user == user.email) and (input_password != user.password):
        flash('Incorrect email or password.')
        return redirect('/')

    else:
        if not argon2.verify(input_password, user.password):
            flash('Incorrect email or password.')
            return redirect('/')

        elif argon2.verify(input_password, user.password):
            session['EMAIL'] = user.email
            session['FNAME'] = user.fname 
            session['LNAME'] = user.lname
            session['ID'] = user.user_id
            session['queried_playlist'] = None
            return redirect ('/search')

        else:
            flash('Please sign up or try again.')
            redirect('/')
 

@app.route('/search')
def search_artists():
    """ Main dashboard for searching for similar artists """

    return render_template('searchhome.html')


@app.route('/logout')
def logout_user():
    """ Logs out user """

    session.clear()
    return redirect('/')
 

@app.route('/users/profile/<fname>')
def show_user_profile(fname):
    """ Displays user profile and saved user playlists """   

    playlists = crud.get_saved_playlists(crud.get_user_by_email(session['EMAIL']).user_id)
    playlist_ids = crud.get_user_playlist_ids(crud.get_user_by_email(session['EMAIL']).user_id)
    playlists_and_playlist_ids = helper.create_dict_playlists_playlistids(playlists, playlist_ids)

    return render_template('profile.html', 
                            fname=fname, 
                            playlists_and_playlist_ids=playlists_and_playlist_ids)


@app.route('/users/profile/api')
def get_user_information():

    user = crud.get_user_by_email(session['EMAIL'])
    return jsonify({'fname': user.fname, 'lname': user.lname, 'email': user.email})  


@app.route('/new-playlist', methods=['POST'])
def generate_playlist():
    """ Generates a playlist based on a given artist """
    
    form_artist = request.form.get('form_artist')
    queried_artist = form_artist.title()
    
    # LAST FM endpoint for getting similar artists - API Call #1
    url1 = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar'

    payload = {'artist': form_artist,
               'api_key': LASTFM_API_KEY,
               'format': 'json',
               'limit' : 15}

    response = requests.get(url1, params=payload)
    data = response.json()
   
    top_track_list = []
    similar_artists_list = []
    for i in range (15):
        similar_artists = (data['similarartists']['artist'][i])['name']
        similar_artists_list.append(similar_artists)
        similar_artists_list.append(similar_artists)
    
    # LAST FM endpoint for getting artist's Top Tracks - API Call #2
    url2 = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks'

    # Loops through the similar artists list and inserts into payload
    for artist in data['similarartists']['artist']:
       
        payload2 = {'artist': artist['name'],
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

    sim_artists_and_top_tracks = helper.create_dict_sim_artists_top_tracks(similar_artists_list, top_track_list)
    track_duration_list = [] # milliseconds

     # LAST FM endpoint for getting artist's Top Tracks - API Call #3
    url3 = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo'

    for artist in sim_artists_and_top_tracks.keys():
        for track in sim_artists_and_top_tracks[artist]:

            payload3 = {'api_key': LASTFM_API_KEY,
                        'artist': artist,
                        'track': track,
                        'format': 'json'}

            response3 = requests.get(url3, params=payload3)
            track_dur_data = response3.json() 
            
            track_duration = track_dur_data['track']['duration']
            track_duration_list.append(track_duration)
    
    
    conv_track_lengths = helper.convert_millis(track_duration_list)
    playlist_query_list = helper.create_artist_track_dur_list(similar_artists_list, top_track_list, conv_track_lengths)
    crud.create_many_tracks(similar_artists_list, top_track_list, conv_track_lengths)
    session['queried_playlist'] = playlist_query_list
    
    return render_template('new_playlist.html', 
                            similar_artists_list=similar_artists_list,
                            top_track_list=top_track_list,
                            conv_track_lengths=conv_track_lengths, 
                            queried_artist=queried_artist)


@app.route('/playlists', methods=['GET'])
def show_saved_playlist():
    """ Displays list of saved playlists """

    playlists = crud.get_saved_playlists(crud.get_user_by_email(session['EMAIL']).user_id)
    playlist_ids = crud.get_user_playlist_ids(crud.get_user_by_email(session['EMAIL']).user_id)
    playlists_and_playlist_ids = helper.create_dict_playlists_playlistids(playlists, playlist_ids)
    
    return render_template('savedplaylists.html', 
                            playlists_and_playlist_ids=playlists_and_playlist_ids)


@app.route('/playlists', methods=['POST'])
def save_my_playlist():
    """ Displays list of saved playlists """

    playlist_name = request.form.get('save_playlist_form')
    save_playlist = request.args.get('save_playlist_btn')
    saved_playlist = crud.create_playlist(crud.get_user_by_email(session['EMAIL']), playlist_name)
    playlist_id = saved_playlist.playlist_id
    playlist = session['queried_playlist'] 
    
    playlist_track_list = [] 
    for tracks in playlist:
        playlist_track_list.append(tracks[1])
    
    for track in playlist_track_list:
        crud.create_playlist_track(saved_playlist.playlist_id, crud.get_track_id(track))
    return redirect('/playlists')
   

@app.route('/playlists/<playlist_id>')
def show_playlist_by_id(playlist_id):
    """ Save playlist to profile """

    playlist_name = crud.get_playlist_name(playlist_id)
    track_objs = crud.get_playlist_tracks(playlist_id)
    
    tracks = crud.get_many_tracks_by_track_obj(track_objs)
    artists = crud.get_many_artists_by_track_obj(track_objs)
    track_durs = crud.get_many_durs_by_track_obj(track_objs)

    return render_template('playlist_id.html', 
                            playlist_name=playlist_name,
                            artists=artists,
                            tracks=tracks,
                            track_durs=track_durs)


@app.route('/about-radlist')
def show_about():
    """Displays about page for RAD List"""

    return render_template('about_radlist.html')




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0") 