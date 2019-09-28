import networkx as nx
from graph_food_optimization import *
from crop_prediction import *
from forecaster import forecaster as fc


def formatted_print(iterable, header):
    max_len = [len(x) for x in header]
    for row in iterable:
        for index, col in enumerate(row):
            if max_len[index] < len(str(col)):
                max_len[index] = len(str(col))
    output = '-' * (sum(max_len) + 1) + '\n'
    output += '|' + ''.join([h + ' ' * (l - len(h)) + '|' for h, l in zip(header, max_len)]) + '\n'
    output += '-' * (sum(max_len) + 1) + '\n'
    for row in iterable:
        output += '|' + ''.join([str(c) + ' ' * (l - len(str(c))) + '|' for c, l in zip(row, max_len)]) + '\n'
    output += '-' * (sum(max_len) + 1) + '\n'
    print(output)


def calculate_shipping_cost(G, country_name, countries):
    shortest_paths = {}
    for each_country in countries:
        shortest_distance = nx.shortest_path_length(G, country_name, each_country, weight='weight')
        shortest_paths[each_country] = shortest_distance
    return shortest_paths


def find_exports(G, countries_data, crop, printable_data, country_name):
    quantity_exported = countries_data[country_name][crop]
    index = 0
    exports1 = []
    while quantity_exported > 0 and index < len(printable_data):
        q_imported = abs(float(printable_data[index][1]))
        if q_imported >= quantity_exported:
            q = quantity_exported
            quantity_exported -= q
        else:
            q = q_imported
            quantity_exported -= q
        sc = printable_data[index][2]
        path = str(nx.shortest_path(G, country_name, printable_data[index][0], weight='weight')).replace(",", "->")
        exports1.append([printable_data[index][0], "%.2f" % q, path])
        index += 1
    header = ['Country', 'Quantity(tons)', 'Path']
    formatted_print(exports1, header)


def find_imports(G, countries_data, crop, printable_data, country_name):
    quantity_imported = abs(float(countries_data[country_name][crop]))
    index = 0
    imports1 = []
    while quantity_imported > 0 and index < len(printable_data):
        q_exported = abs(float(printable_data[index][1]))
        if quantity_imported <= q_exported:
            q = quantity_imported
            quantity_imported = 0
        else:
            q = q_exported
            quantity_imported -= q
        sc = printable_data[index][2]
        q = "%.2f" % q
        path = str(nx.shortest_path(G, printable_data[index][0], country_name, weight='weight')).replace(",", "->")
        imports1.append([printable_data[index][0], q, path])
        index += 1
    header = ['Country', 'Quantity(tons)', 'Path']
    formatted_print(imports1, header)


def calculate_profitability_export(demand, shipping_cost):
    profit = {}
    for country in demand.keys():
        profit[country] = (0.9 * abs(demand[country])) + (0.1 * shipping_cost[country])
    return profit


def exports(G, countries_data, country_name, crop):
    print("\t\t\tExport", crop)
    quantity_exported = countries_data[country_name][crop]
    print("Quantity to be exported (tons): ", "%.2f" % quantity_exported)
    demand = {}
    for country in countries_data.keys():
        if countries_data[country][crop] < 0:
            demand[country] = countries_data[country][crop]
    demand_dict = demand
    demand = sorted(demand.items(), key=lambda kv: kv[1])
    shipping_costs = calculate_shipping_cost(G, country_name, [row[0] for row in demand])
    profitability = calculate_profitability_export(demand_dict, shipping_costs)
    profitability1 = sorted(profitability.items(), key=lambda kv: kv[1], reverse=True)
    printable_data = []
    header = ['Country', 'Demand(tons)', 'Shipping Cost', 'Profitability']
    for key in demand_dict.keys():
        printable_data.append([key, "%.2f" % demand_dict[key], "%.2f" % shipping_costs[key], "%.2f" % profitability[key]])
    printable_data.sort(key=lambda x: abs(float(x[3])), reverse=True)
    formatted_print(printable_data, header)
    find_exports(G, countries_data, crop, printable_data, country_name)


def imports(G, countries_data, country_name, crop):
    print("\t\t\tImport", crop)
    quantity_imported = countries_data[country_name][crop]
    print("Quantity to be imported (tons): ", "%.2f" % quantity_imported)
    demand = {}
    for country in countries_data.keys():
        if countries_data[country][crop] > 0:
            demand[country] = countries_data[country][crop]
    demand_dict = demand
    demand = sorted(demand.items(), key=lambda kv: kv[1])
    shipping_costs = calculate_shipping_cost(G, country_name, [row[0] for row in demand])
    profitability = calculate_profitability_export(demand_dict, shipping_costs)
    profitability1 = sorted(profitability.items(), key=lambda kv: kv[1], reverse=True)
    printable_data = []
    header = ['Country', 'Demand(tons)', 'Shipping Cost', 'Profitability']
    for key in demand_dict.keys():
        printable_data.append([key, "%.2f" % demand_dict[key], "%.2f" % shipping_costs[key], "%.2f" % profitability[key]])
    printable_data.sort(key=lambda x: abs(float(x[3])), reverse=True)
    formatted_print(printable_data, header)
    find_imports(G, countries_data, crop, printable_data, country_name)


def crop_optimization(G, countries_data, country_name):
    country_data = countries_data[country_name]
    for crop in country_data.keys():
        if country_data[crop] > 0:
            exports(G, countries_data, country_name, crop)
        else:
            imports(G, countries_data, country_name, crop)
        print("-"*100)


def optimization(G, data, country_name):
    countries = {}
    for row in data:
        sub_dictionary = {'millets': row[1], 'rice': row[2], 'wheat': row[3]}
        countries[row[0]] = sub_dictionary
    crop_optimization(G, countries, country_name)


G = design_graph()
country_name, year = input('Enter Country Name and Year for food logistics optimization : ').strip().split(' ')
year = int(year)
fc(country_name)
food, raw_data = print_data(year)
optimization(G, raw_data, country_name)
