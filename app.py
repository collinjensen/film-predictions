from flask import Flask
from markupsafe import escape
from functions import make_prediction

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/predict/<path:url>")
def predict(url):
    prediction = make_prediction(url)
    return f"<p>{prediction}</p>"