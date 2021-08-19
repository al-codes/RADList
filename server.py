from flask import Flask, render_template
from model import connect_to_db
import crud
import requests, jinja2, os

app = Flask(__name__)

app.secret_key = 'POTATO'
app.jinja_env.undefined = jinja2.StrictUndefined
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True
API_KEY = os.environ['LASTFM_KEY']

@app.route("/")
def index():
    """Landing page"""
  
    return render_template("homepage.html")

#############################################
# USER LOGIN INFO
@app.route("/signup")
def signup_user():
    """Shows user sign up form"""

    return render_template("signup.html")

@app.route("/login")
def login_user():
    """Shows user login form"""

    return render_template("login.html")


#############################################
@app.route("/user-profile")
def show_profile():
    """Displays user profile"""

    return render_template("profile.html")


@app.route("/new-playlist")
def generate_playlist():
    """Displays generated playlist"""

    return render_template("new_playlist.html")

@app.route("/saved-playlists")
def show_playlists():
    """Displays saved playlists saved by user"""

    return render_template("playlists.html")

@app.route("/about-radlist")
def show_about():
    """Displays about page for RAD List"""

    return render_template("about_radlist.html")








if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    import sys
    app.run(host="0.0.0.0", debug=True)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0")