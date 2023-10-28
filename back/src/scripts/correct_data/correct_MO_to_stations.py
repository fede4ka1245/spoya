import pandas as pd


def correct_MO_to_stations(MO_to_weather_stations):
    # print(MO_to_weather_stations)
    MO_to_weather_stations = {x: y.split()[1] for x, y in MO_to_weather_stations.items()}
    # print(MO_to_weather_stations)

    meteostations_to_replace = {
        "Большая": "Большая Соснова",
        "Кочёво": "Кочево",
    }

    for key, value in MO_to_weather_stations.items():
        if key in meteostations_to_replace:
            MO_to_weather_stations[key] = meteostations_to_replace[key]
    return MO_to_weather_stations
