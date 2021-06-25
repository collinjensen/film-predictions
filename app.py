from flask import Flask
from markupsafe import escape
from functions import make_prediction, get_wrangle, get_data

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/predict/<path:url>")
def predict(url):
    prediction = make_prediction(url)
    return f"<p>{prediction}</p>"

@app.route("/wrangle/<path:url>")
def wrangle(url):
    wrangled = get_wrangle(url)
    return f"<p>{wrangled}</p>"

@app.route("/data/<path:url>")
def data(url):
    got_data = get_data(url)
    return f"<p>{got_data}</p>"
