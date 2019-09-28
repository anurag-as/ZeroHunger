import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
from scipy import stats

land_data = pd.read_csv("Temperature.csv")


def save_model(country_name, model):
    filename = 'model.sav'
    dir_path = os.getcwd()
    try:
        os.mkdir(dir_path + "//" + "Temperature_data")
        
    except:
        pass

    try:
        os.mkdir(dir_path + "//Temperature_data" + "//" + country_name)
    except:
        pass
    file_path = dir_path + "//" + "Temperature_data" + "//" + country_name + "//" + filename
    print(file_path)
    pickle.dump(model, open(file_path, 'wb'))


def get_country_rows(country_name):
    country_data = land_data[land_data['Area'] == country_name]
    return country_data


data = pd.read_csv('Temperature.csv')


def predict(model, X_test, y_test):
    y_pred = model.predict(X_test)
    for i in range(len(y_test)):
        print(y_pred[i], y_test[i])


def train(country_name, start_row, end_row):
    print(data.shape)
    print(data.describe)

    X = data[['Area Code', 'Year']].values[start_row:end_row]
    y = data[['Value']].values[start_row:end_row]
    plt.scatter(data['Year'][start_row:end_row], y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    save_model(country_name, model)
    print("-"*100)
    print(country_name)
    predict(model, X_test, y_test)
    print("-"*100)


def get_input():
    country_name, year = input('Enter Country Name and Year').strip().split(' ')
    year = int(year)
    return country_name, year


def get_country_code(data):
    country_code = country_rows.iloc[0]['Area Code']
    return country_code


def get_row_numbers(data):
    start_row = country_rows.index[0] + 1
    end_row = country_rows.index[-1] + 2
    return start_row, end_row


def get_all_country_names():
    return land_data.Area.unique()


for country_name in get_all_country_names():
    country_rows = get_country_rows(country_name)
    start_row, end_row = get_row_numbers(country_rows)
    country_code = get_country_code(country_rows)
    train(country_name, start_row, end_row)
