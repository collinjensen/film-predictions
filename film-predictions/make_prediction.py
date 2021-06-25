import pickle
import pandas as pd
import requests
import json
from functions import get_wrangle

# loading Random Forest Regressor model through pickle
random_forest_regressor_filename = 'random_forest_regressor_20210623.pkl'
random_forest_regressor_pkl = open(random_forest_regressor_filename, 'rb')
random_forest_regressor = pickle.load(random_forest_regressor_pkl)

# taking input
movie_url = input('IMDb URL:')

# preprocessing
movie = get_wrangle(movie_url)

# making prediction
predicted = random_forest_regressor.predict(movie)[0]
rounded = round(predicted * 2) / 2 # rounds prediction to nearest 0.5 (/5 stars)

# print result
print(rounded, 'stars')
