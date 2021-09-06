""" Server for RAD List """

from flask import Flask, render_template, redirect, request, session, flash, jsonify
from jinja2 import StrictUndefined
from model import connect_to_db, User, Playlist, Track
import requests
import crud 
import helper
import os
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
        return redirect('/search')
    
    else:
        return render_template('homepage.html')



@app.route('/users/create-user.json', methods=['POST'])
def signup_user():
    """ Process user signup form """
    
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email = email).first()

    # If email exists in db, redirect to homepage
    if user != None:
        flash('This email is already taken.')
        return jsonify('This email is already taken.')

    # If user email/pass is already in the db
    elif user != None and user.email == email and user.password == password:
        flash('This email and password already exists. Please go to Login to sign in.')
        return jsonify('This email and password already exists. Please go to Login to sign in.')
    # If a new user and all correct
    else:
        # Add new user
        new_user = crud.create_user(fname, lname, email, password)

        # Saving user to session
        user = crud.get_user_by_email(email) 
        session['EMAIL'] = user.email
        session['FNAME'] = user.fname 
        session['LNAME'] = user.lname
        session['ID'] = user.user_id
        flash('You have registered successfully.')
        return jsonify('You have registered successfully. Please log in.')



@app.route('/login', methods=['POST'])
def process_login():
    """ Logs in a user """
  
    # Get email and password from Login form
    email = request.form.get('email')
    input_password = request.form.get('password')

    # Gets user by email entered in login form
    user = crud.get_user_by_email(email) 

    # If user does not exist
    if user == None:
        flash('Email does not exist. Please sign up or try again.')
        return redirect('/')
    
    # If user exists and password matches, show success and take to profile
    else:
        if argon2.verify(input_password, user.password):
            session['EMAIL'] = user.email
            session['FNAME'] = user.fname 
            session['LNAME'] = user.lname
            session['ID'] = user.user_id
            session['saved_playlist'] = None
            flash('You have successfully logged in.')
            return redirect ('/search')

        else:
            flash('Incorrect Password. Please try again.')
            return redirect ('/')   
      


@app.route('/search')
def search_artists():
    """ Search for similar artists """

    return render_template('searchhome.html')



@app.route('/logout')
def logout_user():
    """ Logs out user """

    session.clear()

    return redirect('/')
 


@app.route('/users/profile/<fname>')
def show_user_profile(fname):
    """ Displays user profile """   

    if not session:
        flash('Please login to view profile.')
        return redirect('/login')

    else:
        return render_template('profile.html', fname=fname)



@app.route('/new-playlist', methods=['POST'])
def generate_playlist():
    """ Generates a playlist based on a given artist """
    
    # Get artist from form on homepage.html
    form_artist = request.form.get('form_artist')
    

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

    # List of 15 similar artists for template
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
     

        # Response from second API call for Top Tracks
        response2 = requests.get(url2, params=payload2)
        artist_data = response2.json() 
        
        
        # Top 2 Tracks
        track_name_1 = artist_data['toptracks']['track'][0]['name']
        track_name_2 = artist_data['toptracks']['track'][1]['name']
        top_track_list.append(track_name_1)
        top_track_list.append(track_name_2)


    # Create dictionary of new playlist output for API Call #3
    sim_artists_and_top_tracks = {}
    for i in range(len(similar_artists_list)):
        if similar_artists_list[i] in sim_artists_and_top_tracks:
            sim_artists_and_top_tracks[similar_artists_list[i]].append(top_track_list[i])
        else:
            sim_artists_and_top_tracks[similar_artists_list[i]] = [top_track_list[i]]
    

    track_duration_list = [] # Times in milliseconds. need to convert with crud fcn.

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
    
    # Convert tracks from milliseconds to 00:00:00 format
    conv_track_lengths = crud.convert_millis(track_duration_list)
    
    # similar_artists_list = []
    # top_track_list = []
    # conv_track_lengths = []
    playlist_query_list = helper.create_artist_track_dur_list(similar_artists_list, top_track_list, conv_track_lengths)
   
    # Add tracks to db
    for i in range(len(top_track_list)):
        crud.create_track(top_track_list[i], similar_artists_list[i], conv_track_lengths[i])

    # Save playlist info to session 
    session['queried_playlist'] = playlist_query_list
    
    
    # Track times will show but not saved in session/tracks
    return render_template('new_playlist.html', 
                            similar_artists_list=similar_artists_list,
                            top_track_list=top_track_list,
                            conv_track_lengths=conv_track_lengths)



@app.route('/playlists', methods=['GET'])
def show_saved_playlist():
    """ Displays list of saved playlists """
    # Add logic if user not in session flash msg to log in
    if not session:
        flash('You must sign in to save/view playlists.')
        return redirect("/")

    playlists = crud.get_saved_playlists(crud.get_user_by_email(session['EMAIL']).user_id)
    playlist_ids = crud.get_user_playlist_ids(crud.get_user_by_email(session['EMAIL']).user_id)
    
    playlists_and_playlist_ids = {}

    for i in range(len(playlists)):
        playlists_and_playlist_ids[playlists[i]] = playlist_ids[i]


    return render_template('savedplaylists.html', 
                            playlists_and_playlist_ids=playlists_and_playlist_ids)



@app.route('/playlists', methods=['POST'])
def save_my_playlist():
    """ Displays list of saved playlists """
    

    playlist_name = request.form.get('save_playlist_form')
    save_playlist = request.args.get('save_playlist_btn')

    saved_playlist = crud.create_playlist(crud.get_user_by_email(session['EMAIL']), playlist_name)
    playlist_id = saved_playlist.playlist_id

    # get tracks from queried session playlist
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
    
    tracks = []
    artists = []
    track_durs = []

    for track in track_objs:
        artist = crud.get_artist_by_track_id(track.track_id) 
        track = crud.get_title_by_track_id(track.track_id)  
        artists.append(artist)
        tracks.append(track)
       
    # Had to separate from above loop for track time
    for track in track_objs:
        dur = crud.get_track_dur(str(track.track_id))
        track_durs.append(dur)

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
    import sys
    app.run(host="0.0.0.0", debug=True)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0") 