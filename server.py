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
    url1 = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=cher&api_key=d39bc6865aba965b8a8e4f8ec2dc6276&format=json'
    # http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=cher&api_key=YOUR_API_KEY&format=json
    url2 = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=cher&api_key=d39bc6865aba965b8a8e4f8ec2dc6276&format=json'
    res1 = requests.get(url1)
    res2 = requests.get(url2)
    data1 = res1.json()
    data2 = res2.json()

    
    return render_template("homepage.html", data1=data1, data2=data2)
    # return render_template("homepage.html")

# LOGIN from shopping-site further study
# @app.route("/login", methods=["GET"])
# def show_login():
#     """Show login form."""

#     return render_template("login.html")

# @app.route('/login', method=['POST'])
# def user_login():
#     """ User log in"""

#     fname = request.form.get('fname')
#     lname = request.form.get('lname')
#     email = request.form.get('email')
#     password = request.form.get('password')
#  Find the user's login credentials located in the 'request.form'
#  dictionary, look up the user, and store them in the session.
# # # The logic here should be something like:
# #
# # - get user-provided name and password from request.form
# # - use customers.get_by_email() to retrieve corresponding Customer
# #   object (if any)
# # - if a Customer with that email was found, check the provided password
# #   against the stored one
# # - if they match, store the user's email in the session, flash a success
# #   message and redirect the user to the "/melons" route
# # - if they don't, flash a failure message and redirect back to "/login"
# # - do the same if a Customer with that email doesn't exist

# return "Oops! This needs to be implemented"



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    import sys
    app.run(host="0.0.0.0", debug=True)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0")