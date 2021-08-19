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
  
    return render_template("homepage.html")


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    import sys
    app.run(host="0.0.0.0", debug=True)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0")