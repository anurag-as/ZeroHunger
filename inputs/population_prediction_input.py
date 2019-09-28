import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
from scipy import stats

land_data = pd.read_csv("Population_input.csv")


def load_model(country_name):
    filename = 'model.sav'
    dir_path = os.getcwd()
    file_path = dir_path + "/inputs/" + "Population_data" + "/" + country_name + "/" + filename
    loaded_model = pickle.load(open(file_path, 'rb'))
    return loaded_model


def get_country_rows(country_name):
    country_data = land_data[land_data['Area'] == country_name]
    return country_data


data = pd.read_csv('Population_input.csv')


def predict(model, X_test):
    y_pred= model.predict(X_test)
    return y_pred[0][0]


def get_input():
    country_name, year = input('Enter Country Name and Year\n').strip().split(' ')
    year = int(year)
    return country_name, year


def get_country_code(data):
    country_code = data.iloc[0]['Area Code']
    return country_code


def wrapper(country_name, year):
    country_rows = get_country_rows(country_name)
    country_code = get_country_code(country_rows)
    model = load_model(country_name)
    value = predict(model, np.array([[country_code, year]]))
    return value


