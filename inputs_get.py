from inputs import land_prediction_input as li
from inputs import fertilizers_prediction_input as fi
from inputs import livestock_prediction_input as si
from inputs import temperature_prediction_input as ti
from inputs import population_prediction_input as pi


def get_inputs(country_name, year):
    land_input = li.wrapper(country_name, year)
    fertilizer_input = fi.wrapper(country_name, year)
    livestock_input = si.wrapper(country_name, year)
    temperature_input = ti.wrapper(country_name, year)
    return land_input, fertilizer_input, livestock_input, temperature_input


def population_prediction(country_name, year):
    return pi.wrapper(country_name, year)

