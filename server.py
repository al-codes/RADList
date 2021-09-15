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
        flash('This account does not exist. Please sign up or try again.')
        return redirect('/')

    elif argon2.verify(input_password, user.password):
        session['EMAIL'] = user.email
        session['FNAME'] = user.fname 
        session['LNAME'] = user.lname
        session['ID'] = user.user_id
        session['queried_playlist'] = None
        return redirect ('/search')

    elif TypeError:
        flash('Incorrect email or password.')
        return redirect('/')

    else:
        flash('Please sign up or try again.')
        redirect('/')


@app.route('/search')
def search_artists():
    """ Main dashboard for searching for similar artists """
    
    if not session:
        return redirect('/')
    else:
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

    similar_artists_list = lastfm_api.get_similar_artists(form_artist)
    top_track_list = lastfm_api.get_top_tracks(similar_artists_list)
    sim_artists_and_top_tracks_dict = helper.create_dict_sim_artists_top_tracks(similar_artists_list, top_track_list)
    track_duration_list = lastfm_api.get_track_durations(sim_artists_and_top_tracks_dict)
    conv_track_lengths = helper.convert_millis(track_duration_list)

    playlist_query_dict = helper.create_dict_sim_artists_top_tracks_duration(similar_artists_list, top_track_list, conv_track_lengths)
    crud.create_many_tracks(similar_artists_list, top_track_list, conv_track_lengths)
    session['queried_playlist'] = playlist_query_dict

    return render_template('new_playlist.html', 
                            playlist_query_dict=playlist_query_dict, 
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
    saved_playlist = crud.create_playlist(crud.get_user_by_email(session['EMAIL']), playlist_name)
    playlist_id = saved_playlist.playlist_id
    playlist = session['queried_playlist'] 


    playlist_track_list = [] 
    for tracks in playlist.values():
        playlist_track_list.append(tracks[0])
        playlist_track_list.append(tracks[2])
  
    for track in playlist_track_list:
        crud.create_playlist_track(saved_playlist.playlist_id, crud.get_track_id(track))
    return redirect('/playlists')
   

@app.route('/playlists/<playlist_id>')
def show_playlist_by_id(playlist_id):
    """ Save playlist to profile """

    playlist_name = crud.get_playlist_name(playlist_id)
    playlist_dict = helper.get_user_playlist_details_by_pid(playlist_id)

    return render_template('playlist_id.html',
                            playlist_name=playlist_name,
                            playlist_dict=playlist_dict)


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