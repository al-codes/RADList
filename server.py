from flask import Flask, render_template
from model import connect_to_db
import crud
# import requests
import jinja2
# import os

app = Flask(__name__)

# app.secret_key = 'POTATO'

# app.jinja_env.undefined = jinja2.StrictUndefined

# app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

# API_KEY = os.environ['LASTFM_KEY']

@app.route("/")
def index():
    
    # url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=Spirit+Of...&api_key=d39bc6865aba965b8a8e4f8ec2dc6276&format=json'
    # res = requests.get(url)
    # data = res.json()

    
    # return render_template("homepage.html", data=data)
    return render_template("homepage.html")




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")