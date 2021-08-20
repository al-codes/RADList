from flask import (Flask, render_template, redirect, request, session, flash, 
                    jsonify)
from jinja2 import StrictUndefined
from model import connect_to_db, User, Playlist, Track
import crud #comment out if you want to -i into crud.py
import os


app = Flask(__name__)

app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True
LASTFM_API_KEY = os.environ['LASTFM_KEY']


######### ROUTES ###############

@app.route('/')
def index():
    """ Display homepage """
  
    return render_template('homepage.html')



#############################################
# USER SIGNUP/LOGIN ROUTES

@app.route('/signup')
def signup_user():
    """ Signs up a user """
    
    # Something similar to this:
    # fname = request.form['fname']
    # lname = request.form['lname']
    # email = request.form['email']
    # password = request.form['password']

    return render_template('signup.html')



@app.route('/login', methods=['GET']) # what is needed here? get or post? is get needed at all?
def show_login():
    """ Shows user login form """

    return render_template('login.html')



@app.route('/login', methods=['POST'])
def process_login():
    """ Logs in user """

    # Something similar to this logic:

    email = request.form['email']
    password_input = request.form['password']

    user = crud.get_user_by_email(email) # created fcn in crud.py

    if user == None:
        flash('Email does not exist. Please try again.')
        return redirect('/')
    
    else:
        if password_input ==  user.password:
            session['EMAIL'] = user.email
            session['NAME'] = user.fname 
            session['ID'] = user.user_id
            return redirect (f'/user-profile/{user.fname}')  

        else:
            flash('Incorrect Password. Please try again.')
            return redirect ('/')                     


    
@app.route ('/logout')
def logout_user():
    """ Logs out user """

    session.clear()

    return redirect('/')

#############################################


@app.route('/user-profile')
def show_profile():
    """Displays user profile"""

    return render_template('profile.html')


@app.route('/new-playlist')
def generate_playlist():
    """Displays generated playlist"""

    return render_template('new_playlist.html')

@app.route('/saved-playlists')
def show_playlists():
    """Displays saved playlists saved by user"""

    return render_template('playlists.html')

@app.route('/about-radlist')
def show_about():
    """Displays about page for RAD List"""

    return render_template('about_radlist.html')



# What should this actually look like?
if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    import sys
    app.run(host="0.0.0.0", debug=True)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0") 