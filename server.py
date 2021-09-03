""" Server for RAD List """

from flask import Flask, render_template, redirect, request, session, flash
from jinja2 import StrictUndefined
from model import connect_to_db, User, Playlist, Track
import requests
import crud 
import os
from passlib.hash import argon2



app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True
LASTFM_API_KEY = os.environ['LASTFM_KEY']



@app.route('/')
def index():
    """ Display homepage """

    return render_template('homepage.html')



@app.route('/signup', methods=['GET'])
def show_signup():
    """ Displays user signup form """

    return render_template('signup.html')



@app.route('/signup', methods=['POST'])
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
        return redirect('/signup')

    # If user email/pass is already in the db
    elif user != None and user.email == email and user.password == password:
        flash('This email and password already exists. Please go to Login to sign in.')

    # If a new user and all correct
    else:
        # Add new user
        new_user = crud.create_user(fname = fname, 
                                    lname = lname, 
                                    email = email,
                                    password = password)
       
        crud.db.session.add(new_user)
        crud.db.session.commit()

        # Saving user to session
        user = crud.get_user_by_email(email) 
        session['EMAIL'] = user.email
        session['FNAME'] = user.fname 
        session['LNAME'] = user.lname
        session['ID'] = user.user_id
        print('success')
        flash('You have registered successfully.')
        return redirect ('/')



@app.route('/login', methods=['GET']) 
def show_login():
    """ Shows user login form """

    return render_template('login.html')



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
        return redirect('/login')
    
    # If user exists and password matches, show success and take to profile
    else:
        if argon2.verify(input_password, user.password):
            session['EMAIL'] = user.email
            session['FNAME'] = user.fname 
            session['LNAME'] = user.lname
            session['ID'] = user.user_id
            session['saved_playlist'] = None
            print('success')
            flash('You have successfully logged in.')
            return redirect ('/')

        else:
            flash('Incorrect Password. Please try again.')
            return redirect ('/login')   
      
    

@app.route ('/logout')
def logout_user():
    """ Logs out user """

    session.clear()

    return redirect('/')



@app.route('/profile')
def show_user_profile():
    """ Displays user profile """   

    # If user clicks on profile and not signed in   
    if not session:
        flash('Please login to view profile.')
        return redirect('/login')

    else:
        return render_template('profile.html')




# For /new-playlist and /playlists routes
TOP_TRACKS = []
SIMILAR_ARTISTS_LIST = []


@app.route('/new-playlist', methods=['POST'])
def generate_playlist():
    """ Generates a playlist based on a given artist """
    
    # Get artist from form on homepage.html
    form_artist = request.form.get('form_artist')
    

    # LAST FM endpoint for getting similar artists
    url1 = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar'


    payload = {'artist': form_artist,
               'api_key': LASTFM_API_KEY,
               'format': 'json',
               'limit' : 15}

    response = requests.get(url1, params=payload)
    data = response.json()
   


    # List of 15 similar artists for template
    for i in range (15):
        similar_artists = (data['similarartists']['artist'][i])['name']
        SIMILAR_ARTISTS_LIST.append(similar_artists)
   
    

    # LAST FM endpoint for getting artist's Top Tracks
    url2 = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks'

    
    # A dict of artists and tracks
    artists = {}
    
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
        TOP_TRACKS.append(track_name_1)
        TOP_TRACKS.append(track_name_2)


       
        crud.create_track(track_name_1, artist['name'])
        crud.create_track(track_name_2, artist['name'])
        

   
    return render_template('new_playlist.html', 
                            data=artists,
                            SIMILAR_ARTISTS_LIST=SIMILAR_ARTISTS_LIST,
                            TOP_TRACKS=TOP_TRACKS)



# Not an intended feature but keeping for now
@app.route('/newplaylist/details', methods=['GET'])
def show_last_search():
    """ Displays last search """

    if session and session['saved_playlist'] == None:
        flash('You must first save a playlist to view saved playlists.')
        return redirect("/")
    
    if not session:
        flash('You must sign in to save/view playlists.')
        return redirect("/")

    return render_template("/playlistdetails.html")




@app.route('/playlists', methods=['GET'])
def show_saved_playlist():
    """ Displays list of saved playlists """

     
    playlists = crud.get_saved_playlists(crud.get_user_by_email(session['EMAIL']).user_id)
    playlist_ids = crud.get_user_playlist_ids(crud.get_user_by_email(session['EMAIL']).user_id)
    
    playlists_and_playlist_ids = {}
    
    for playlist in playlists:
        for playlist_id in playlist_ids:
            playlists_and_playlist_ids[playlist] = playlist_id
    
   # Jinja template - all links have same playlist_id
    

    return render_template('savedplaylists.html', 
                            playlists_and_playlist_ids=playlists_and_playlist_ids)



@app.route('/playlists', methods=['POST'])
def save_my_playlist():
    """ Displays list of saved playlists """
    

    playlist_name = request.form.get('save_playlist_form')
    save_playlist = request.args.get('save_playlist_btn')

    saved_playlist = crud.create_playlist(crud.get_user_by_email(session['EMAIL']), playlist_name)
    playlist_id = saved_playlist.playlist_id

    for track in TOP_TRACKS:
        crud.create_playlist_track(saved_playlist.playlist_id, crud.get_track_id(track))


    return redirect('/playlists')
   


@app.route('/playlists/<playlist_id>')
def show_playlist_by_id(playlist_id):
    """ Save playlist to profile """

    playlist_name = crud.get_playlist_name(playlist_id)

    track_objs = crud.get_playlist_tracks(playlist_id)

    # artists = {}
    # Write dictionary instead of appending to two lists?
    # Values can be overwritten - how to add to values 
    # for track in track_obj:
    #     artist = crud.get_artist_by_track_id(track.track_id)   
    #     track = crud.get_title_by_track_id(track.track_id)
    #     artists[artist] = track
    #     artists[artist] = []
    #     artists[artist].append(track)
    
    
    tracks = []
    artists = []
    for track in track_objs:
        artist = crud.get_artist_by_track_id(track.track_id) 
        track = crud.get_title_by_track_id(track.track_id)  
        artists.append(artist)
        tracks.append(track)
    

    return render_template('playlist_id.html', 
                            playlist_name=playlist_name,
                            artists=artists,
                            tracks=tracks)



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