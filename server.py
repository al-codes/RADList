""" Server for RAD List """

from flask import (Flask, render_template, redirect, request, session, 
                   flash, jsonify)
from jinja2 import StrictUndefined
from model import (connect_to_db, User, Playlist, Track)
import crud 
import os
from passlib.hash import argon2


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
@app.route('/signup', methods=['GET'])
def show_signup():

    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_user():
    """ Signs up a user """
    
    
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email = email).first()

    # If email exists in db, redirect to homepage
    if user != None:
        flash('This email is already taken.')
        return redirect('/')

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
        # might move this function out of crud
        user = crud.get_user_by_email(email) 
        session['EMAIL'] = user.email
        session['NAME'] = user.fname 
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
    """ Logs in and verifies a user """

  
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
            print('success')
            flash('You have successfully logged in.')
            return redirect ('/')

        else:
            flash('Incorrect Password. Please try again.')
            return redirect ('/login')   
           
    # # If user exists but incorrect email/pass
    # elif user != None:
    #     flash('Incorrect email or password.') 

    # # If user/email/password does not exist, try again or sign up. 
    # else:
    #         flash('Email and password not registered. Please check your credentials or sign up.')
    #         return redirect ('/')     


    
@app.route ('/logout')
def logout_user():
    """ Logs out user """

    session.clear()
    return redirect('/')

#############################################


@app.route('/profile')
def show_user_profile():
    """Show logged in user profile"""   

    if not session:
        flash('Please login to view profile.')
        return redirect('/login')
       
    
    else:
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




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    import sys
    app.run(host="0.0.0.0", debug=True)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0") 