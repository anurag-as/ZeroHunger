import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import land_prediction as lpi
from scipy import stats
from inputs_get import *
crop_data = pd.read_csv("crop_data.csv")


def load_model(country_name):
    filename = 'model.sav'
    dir_path = os.getcwd()
    file_path = dir_path + "/" + "crop_data" + "/" + country_name + "/" + filename
    loaded_model = pickle.load(open(file_path, 'rb'))
    return loaded_model


def get_country_rows(country_name):
    country_data = crop_data[crop_data['Area'] == country_name]
    return country_data


data = pd.read_csv('crop_data.csv')


def predict(model, X_test):
    y_pred= model.predict(X_test)
    return y_pred[0][0], y_pred[0][1], y_pred[0][2]


def get_input():
    country_name, year = input('Enter Country Name and Year\n').strip().split(' ')
    year = int(year)
    return country_name, year


def get_country_code(data):
    country_code = data.iloc[0]['Area Code']
    return country_code


def wrapper(country_name, year):
    land_input, fertilizer_input, livestock_input, temperature_input = get_inputs(country_name, year)
    model = load_model(country_name)
    population_predict = int(population_prediction(country_name, year))
    land_predict = lpi.wrapper(country_name, year)
    country_rows = get_country_rows(country_name)
    country_code = get_country_code(country_rows)
    millets, rice, wheat = predict(model, np.array([[country_code, year, land_input, livestock_input, fertilizer_input,
                                      temperature_input]]))
    return millets, rice, wheat, population_predict, land_predict


def eats():
    millets_person = 0.002
    rice_person = 0.060
    wheat_person = 0.080
    return millets_person, rice_person, wheat_person


def formatted_print(iterable, header):
    max_len = [len(x) for x in header]
    for row in iterable:
        row = [row] if type(row) not in (list, tuple) else row
        for index, col in enumerate(row):
            if max_len[index] < len(str(col)):
                max_len[index] = len(str(col))
    output = '-' * (sum(max_len) + 1) + '\n'
    output += '|' + ''.join([h + ' ' * (l - len(h)) + '|' for h, l in zip(header, max_len)]) + '\n'
    output += '-' * (sum(max_len) + 1) + '\n'
    for row in iterable:
        row = [row] if type(row) not in (list, tuple) else row
        output += '|' + ''.join([str(c) + ' ' * (l - len(str(c))) + '|' for c, l in zip(row, max_len)]) + '\n'
    output += '-' * (sum(max_len) + 1) + '\n'
    print(output)


def number_formatter(number):
    if abs(int(number)) > 10 ** 6:
        number = number / 10 ** 6
        return "%.1f Mt" % number
    elif abs(int(number)) > 10**3:
        number = number / 10**3
        return "%.1f kt" % number
    return "%.1f " % number


def calculator(country_name, millets, rice, wheat, millets_person, rice_person, wheat_person, population, land):
    population *= 1000
    if millets < 0:
        millets = 0
    if rice < 0:
        rice = 0
    if wheat < 0:
        rice = 0
    land = "%.1f" % (land/100)
    millets_consumed = millets_person * population
    wheat_consumed = wheat_person * population
    rice_consumed = rice_person * population
    mil_balance = (millets-millets_consumed)/1000
    rice_balance = (rice-rice_consumed)/1000
    wheat_balance = (wheat-wheat_consumed)/1000
    raw_data = [country_name, mil_balance, rice_balance, wheat_balance]
    population = "%.1f" % (population/(10**6))
    mil_balance = number_formatter(mil_balance)
    rice_balance = number_formatter(rice_balance)
    wheat_balance = number_formatter(wheat_balance)
    millets = number_formatter(millets)
    rice = number_formatter(rice)
    wheat = number_formatter(wheat)

    return [country_name, population, land, millets, rice, wheat, mil_balance, rice_balance, wheat_balance], raw_data


def get_all_country_names():
    return data.Area.unique()


def print_data(year):
    header = ['Country', 'Population(millions)', 'Agriculture Land(100 hA)', 'Millets Prod(tons)', 'Rice Prod(tons)', 'Wheat Prod(tons)', 'Millets Balance(tons)', 'Rice Balance(tons)', 'Wheat Balance(tons)']
    food = []
    raw_data_collected = []
    for country_name in get_all_country_names():
        millets, rice, wheat, population, land_prediction = wrapper(country_name, year)
        millets_person, rice_person, wheat_person = eats()
        calculation_surplus, raw_data = calculator(country_name, millets, rice, wheat, millets_person,
                               rice_person, wheat_person, population, land_prediction)
        food.append(calculation_surplus)
        raw_data_collected.append(raw_data)
    print("\t\t\tCountry wise crop data")
    formatted_print(food, header)
    print("-"*100)
    return food, raw_data_collected


