import matplotlib.pyplot as plt
import land_prediction as lpi
import inputs_get as ig
import numpy as np
fig = plt.figure()


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


def plot_graph(plot_data, pos, label):
    plt.ylim(0, max(plot_data)*1.2)
    plt.xlabel('Year')
    plt.ylabel(label)
    plt.plot(range(1960, 2031), plot_data)
    plt.show()


def forecaster(country_name):
    land_data = []
    land_data_year = []
    livestock_data = []
    livestock_data_year = []
    temp_data = []
    temp_data_year = []
    fert_data = []
    fert_data_year = []
    pop_data = []
    pop_data_year = []
    print_data = []
    for year in range(1960, 2031):
        land_input, fertilizer_input, livestock_input, temperature_input = ig.get_inputs(country_name, year)
        pop_input = ig.population_prediction(country_name, year)
        land_data.append(land_input)
        land_data_year.append([land_input, year])
        livestock_data.append(livestock_input)
        livestock_data_year.append([livestock_input, year])
        fert_data.append(fertilizer_input)
        fert_data_year.append([fertilizer_input, year])
        temp_data.append(temperature_input)
        temp_data_year.append([temperature_input, year])
        pop_data.append(pop_input)
        pop_data_year.append([pop_input, year])
        if fertilizer_input < 0:
            fertilizer_input = 0
        fertilizer_input = "%.2f" % (fertilizer_input/10**6)
        if livestock_input < 0:
            livestock_input = 0
        livestock_input = int(livestock_input)
        if temperature_input < 0:
            temperature_input = 0
        land_input = "%.2f" % (land_input/100)
        temperature_input = "%.3f" % temperature_input
        print_data.append([year, land_input, fertilizer_input, livestock_input, temperature_input])
    header = ['Year', 'Agriculture land available(100 hA)', 'Nitrogenous Fertilizers (1000 kg) Used', 'Livestock',
              'Temperature Change °C']
    plot_graph(land_data, 321, "Agriculture land available(hA)")
    plot_graph(livestock_data, 322, "Livestock")
    plot_graph(temp_data, 323, "Temperature Change °C")
    plot_graph(fert_data, 224, "Nitrogenous Fertilizers (kg) Used")
    print("\t\t\tForecasted values for ", country_name, " from 1960 to 2030")
    formatted_print(print_data, header)
    print("-"*100)


