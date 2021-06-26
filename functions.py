import requests
import json
import pandas as pd
import pickle
import os

API_HOST = os.getenv('RAPID_HOST')
API_KEY = os.getenv('RAPID_KEY')
API_URL = os.getenv('RAPID_URL')

# get data from rapidapi
def get_data(url):
    url_split = url.split('/')
    tt = ''
    for chunk in url_split:
        if chunk[:2] == 'tt':
            tt = chunk
    url = API_URL
    querystring = querystring = {"i":tt,"r":"json"}
    headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)

# get and wrangle data from rapidapi
def get_wrangle(url):
    movie_details = get_data(url)
    output = {}
    output['Year'] = 0.0
    output['IMDb'] = 0.0
    output['Rotten Tomatoes'] = 0.0
    output['Metacritic'] = 0.0
    output['BoxOffice'] = 0.0
    output['Runtime'] = 0.0
    output['Rotten Tomatoes'] = 0.0
    output['Metacritic'] = 0.0
    if movie_details['Year'] == "N/A":
        output['Year'] = 0.0
    else:
        output['Year'] = float(movie_details['Year'])
    ratings_sources = [x["Source"] for x in movie_details["Ratings"]]
    for i in range(0, len(ratings_sources)):
        if ratings_sources[i] == "Internet Movie Database":
            ratings_sources[i] = "IMDb"
    ratings_values = [x["Value"] for x in movie_details["Ratings"]]
    for i in range(0, len(ratings_sources)):
        output[ratings_sources[i]] = ratings_values[i]
    if len(ratings_sources) != 0:
        output['IMDb'] = float(output['IMDb'].split('/')[0])*10
        output['Rotten Tomatoes'] = float(output['Rotten Tomatoes'].strip('%'))
        output['Metacritic'] = float(output['Metacritic'].split('/')[0])
    if movie_details['BoxOffice'] == "N/A":
        output['BoxOffice'] = 0.0
    if movie_details['BoxOffice'] != "N/A":
        output['BoxOffice'] = float(movie_details['BoxOffice'].strip('$').replace(',', ''))
    output['Runtime'] = float(movie_details['Runtime'].strip(' min'))
    genre_list = [
        'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
        'Documentary', 'Drama', 'Family', 'Horror', 'Mystery', 'Romance', 'no_genre'
    ]
    if movie_details['Genre'].split(',')[0] in genre_list:
        output[movie_details['Genre'].split(',')[0]] = 1.0
        genre_list.remove(movie_details['Genre'].split(',')[0])
    else:
        output['no_genre'] = 1.0
    for genre in genre_list:
        output[genre] = 0.0
    rated_list = [
        'Approved', 'G', 'N/A', 'PG', 'PG-13', 'R', 'TV-14', 'TV-G', 'TV-MA', 'TV-PG', 'Unrated'
    ]
    if movie_details["Rated"] != "Not Rated":
        output[movie_details['Rated']] = 1.0
        rated_list.remove(movie_details['Rated'])
        for rated in rated_list:
            output[rated] = 0.0
    else:
        output["Unrated"] = 1.0
        rated_list.remove("Unrated")
        for rated in rated_list:
            output[rated] = 0.0
    return [pd.Series(output)]

def make_prediction(movie_url):
    # loading Random Forest Regressor model through pickle
    random_forest_regressor_filename = 'random_forest_regressor_20210623.pkl'
    random_forest_regressor_pkl = open(random_forest_regressor_filename, 'rb')
    random_forest_regressor = pickle.load(random_forest_regressor_pkl)

    # getting and wrangling data
    movie = get_wrangle(movie_url)

    # creating prediction and formatting for output
    predicted = random_forest_regressor.predict(movie)[0]
    rounded = round(predicted * 2) / 2 # this rounds prediction to nearest 0.5

    return rounded
