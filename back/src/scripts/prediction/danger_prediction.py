#!/usr/bin/env python3

import pandas as pd
import numpy as np

from catboost import CatBoostClassifier
from src.scripts.correct_data.correct_MO_to_stations import correct_MO_to_stations

from src.tables import Event

from datetime import datetime

from env import DATABASE


def get_respective_weather_df_from_csv():
    respective_weather_df = pd.read_csv('Данные/Данные по метеостанциям. Соответствие МО.csv')
    respective_weather_df.replace('^\s+', '', regex=True, inplace=True)
    respective_weather_df.replace('\s+$', '', regex=True, inplace=True)
    return respective_weather_df


def get_respective_weather_df_from_sql():
    respective_weather_df_from_db = pd.read_sql("districts", DATABASE, columns=["name", "raw_meteorology_station_name"])
    respective_weather_df_from_db.rename(columns={"name": "Муниципальное образование",
                                                  "raw_meteorology_station_name": "Метеорологическая станция"},
                                         inplace=True)
    return respective_weather_df_from_db


def get_weather_stats_df_from_csv():
    return pd.read_csv("Данные/Данные по метеостанциям.csv", low_memory=False)


def get_weather_stats_df_from_sql():
    weather_stats_df = pd.read_sql("weather", DATABASE)

    weather_stats_df.insert(0, "Местное время", weather_stats_df["time"].dt.strftime("%d.%m.%Y %H:%M"))
    weather_stats_df.drop(columns=["time"], inplace=True)
    return weather_stats_df


def get_prediction():
    # # Load data

    # загружаем данные и убираем лишние пробелы до и после слова
    respective_weather_df = get_respective_weather_df_from_sql()

    # переводим МО в название метеостанции которая отвечает за этот округ
    MO_to_weather_station = dict(respective_weather_df.values)
    MO_to_weather_station = {x: y.split()[1] for x, y in MO_to_weather_station.items()}

    # weather_stats_df = pd.read_csv("../.././Данные/Данные по метеостанциям.csv", low_memory=False)
    weather_stats_df = get_weather_stats_df_from_sql()

    weather_stats_df.replace('^\s+', '', regex=True, inplace=True)
    weather_stats_df.replace('\s+$', '', regex=True, inplace=True)
    weather_stats_df.meteostation = weather_stats_df.meteostation.str.replace("й", "й")  # ненавижу
    weather_stats_df["Местное время"] = pd.to_datetime(weather_stats_df["Местное время"], format="%d.%m.%Y %H:%M")

    selected_columns = ['T', 'Td', 'P', 'Po', 'Pa', 'U', 'DD', 'Ff', 'ff10',
                        'ff3', 'N', 'WW', 'W1', 'W2', 'Tn', 'Tx', 'Cl', 'Nh', 'H', 'Cm',
                        'Ch', 'RRR', 'tR', 'E', 'Tg', "E'"]  # 'sss' 'VV'
    cat_features = ['DD', 'N', 'W1', 'W2', 'WW', 'Cl', 'Nh', 'H', 'Cm', 'Ch', 'E', "E'"]
    inf_columns = ["meteostation", "T", "Td", "P", "Po", "Pa", "U", "DD", "Ff", "ff10", "ff3", "N", "WW", "W1", "W2",
                   "Tn", "Tx", "Cl",
                   "Nh", "H", "Cm", "Ch", "RRR", "tR", "E", "Tg", "E'", "T_lag0", "T_lag1", "T_lag2", "T_lag3",
                   "T_lag4",
                   "T_lag5", "T_lag6", "T_lag7", "T_lag8", "T_lag9", "Td_lag0", "Td_lag1", "Td_lag2", "Td_lag3",
                   "Td_lag4",
                   "Td_lag5", "Td_lag6", "Td_lag7", "Td_lag8", "Td_lag9", "P_lag0", "P_lag1", "P_lag2", "P_lag3",
                   "P_lag4",
                   "P_lag5", "P_lag6", "P_lag7", "P_lag8", "P_lag9", "Po_lag0", "Po_lag1", "Po_lag2", "Po_lag3",
                   "Po_lag4",
                   "Po_lag5", "Po_lag6", "Po_lag7", "Po_lag8", "Po_lag9", "Pa_lag0", "Pa_lag1", "Pa_lag2", "Pa_lag3",
                   "Pa_lag4", "Pa_lag5", "Pa_lag6", "Pa_lag7", "Pa_lag8", "Pa_lag9", "U_lag0", "U_lag1", "U_lag2",
                   "U_lag3",
                   "U_lag4", "U_lag5", "U_lag6", "U_lag7", "U_lag8", "U_lag9", "DD_lag0", "DD_lag1", "DD_lag2",
                   "DD_lag3",
                   "DD_lag4", "DD_lag5", "DD_lag6", "DD_lag7", "DD_lag8", "DD_lag9", "Ff_lag0", "Ff_lag1", "Ff_lag2",
                   "Ff_lag3", "Ff_lag4", "Ff_lag5", "Ff_lag6", "Ff_lag7", "Ff_lag8", "Ff_lag9", "ff10_lag0",
                   "ff10_lag1",
                   "ff10_lag2", "ff10_lag3", "ff10_lag4", "ff10_lag5", "ff10_lag6", "ff10_lag7", "ff10_lag8",
                   "ff10_lag9",
                   "ff3_lag0", "ff3_lag1", "ff3_lag2", "ff3_lag3", "ff3_lag4", "ff3_lag5", "ff3_lag6", "ff3_lag7",
                   "ff3_lag8", "ff3_lag9", "N_lag0", "N_lag1", "N_lag2", "N_lag3", "N_lag4", "N_lag5", "N_lag6",
                   "N_lag7",
                   "N_lag8", "N_lag9", "WW_lag0", "WW_lag1", "WW_lag2", "WW_lag3", "WW_lag4", "WW_lag5", "WW_lag6",
                   "WW_lag7", "WW_lag8", "WW_lag9", "W1_lag0", "W1_lag1", "W1_lag2", "W1_lag3", "W1_lag4", "W1_lag5",
                   "W1_lag6", "W1_lag7", "W1_lag8", "W1_lag9", "W2_lag0", "W2_lag1", "W2_lag2", "W2_lag3", "W2_lag4",
                   "W2_lag5", "W2_lag6", "W2_lag7", "W2_lag8", "W2_lag9", "Tn_lag0", "Tn_lag1", "Tn_lag2", "Tn_lag3",
                   "Tn_lag4", "Tn_lag5", "Tn_lag6", "Tn_lag7", "Tn_lag8", "Tn_lag9", "Tx_lag0", "Tx_lag1", "Tx_lag2",
                   "Tx_lag3", "Tx_lag4", "Tx_lag5", "Tx_lag6", "Tx_lag7", "Tx_lag8", "Tx_lag9", "Cl_lag0", "Cl_lag1",
                   "Cl_lag2", "Cl_lag3", "Cl_lag4", "Cl_lag5", "Cl_lag6", "Cl_lag7", "Cl_lag8", "Cl_lag9", "Nh_lag0",
                   "Nh_lag1", "Nh_lag2", "Nh_lag3", "Nh_lag4", "Nh_lag5", "Nh_lag6", "Nh_lag7", "Nh_lag8", "Nh_lag9",
                   "H_lag0", "H_lag1", "H_lag2", "H_lag3", "H_lag4", "H_lag5", "H_lag6", "H_lag7", "H_lag8", "H_lag9",
                   "Cm_lag0", "Cm_lag1", "Cm_lag2", "Cm_lag3", "Cm_lag4", "Cm_lag5", "Cm_lag6", "Cm_lag7", "Cm_lag8",
                   "Cm_lag9", "Ch_lag0", "Ch_lag1", "Ch_lag2", "Ch_lag3", "Ch_lag4", "Ch_lag5", "Ch_lag6", "Ch_lag7",
                   "Ch_lag8", "Ch_lag9", "RRR_lag0", "RRR_lag1", "RRR_lag2", "RRR_lag3", "RRR_lag4", "RRR_lag5",
                   "RRR_lag6",
                   "RRR_lag7", "RRR_lag8", "RRR_lag9", "tR_lag0", "tR_lag1", "tR_lag2", "tR_lag3", "tR_lag4", "tR_lag5",
                   "tR_lag6", "tR_lag7", "tR_lag8", "tR_lag9", "E_lag0", "E_lag1", "E_lag2", "E_lag3", "E_lag4",
                   "E_lag5",
                   "E_lag6", "E_lag7", "E_lag8", "E_lag9", "Tg_lag0", "Tg_lag1", "Tg_lag2", "Tg_lag3", "Tg_lag4",
                   "Tg_lag5",
                   "Tg_lag6", "Tg_lag7", "Tg_lag8", "Tg_lag9", "E'_lag0", "E'_lag1", "E'_lag2", "E'_lag3", "E'_lag4",
                   "E'_lag5", "E'_lag6", "E'_lag7", "E'_lag8", "E'_lag9"]
    label_to_descr = {'ДТП': 'Атмосферное давление, Температура воздуха, Обледенение',
                      'Опасные природные явления': 'Температура воздуха, Температура точки росы, Атмосферное давление',
                      'Прочие опасности': 'Минимальная температура, Количество осадков',
                      'Взрывы/пожары/разрушения': 'Атмосферное давление, Количество осадков, Видимость',
                      'Аварии с выбросом опасных/токсичных веществ': 'Количество осадков, Атмосферное давление, Облачность',
                      'ЖКХ': 'Температура, Атмосферное давление, Количество осадков, Облачность'}
    target_values = ['ДТП',
                     'Опасные природные явления',
                     'Прочие опасности',
                     'Взрывы/пожары/разрушения',
                     'Аварии с выбросом опасных/токсичных веществ',
                     'ЖКХ']

    timestamps = []
    meteostations = []
    probs = []
    labels = []
    for meteostation in set(weather_stats_df.meteostation):
        meteo_df = weather_stats_df[weather_stats_df['meteostation'] == meteostation]
        meteo_df = meteo_df.sort_values(by=['Местное время'])
        meteo_df['RRR'] = meteo_df['RRR'].map(lambda x: x if x not in ['Осадков нет', 'Следы осадков'] else 0)
        for column in selected_columns:
            for i in range(10):
                meteo_df[f"{column}_lag{i}"] = meteo_df[column].shift(i)
        meteo_df = meteo_df.iloc[-8 * 10:]

        cat_features2 = [column for column in meteo_df.columns if
                         any(map(lambda x: column.startswith(x), cat_features))]
        for cat_feature in cat_features2:
            meteo_df[cat_feature] = meteo_df[cat_feature].fillna('')
            meteo_df[cat_feature] = meteo_df[cat_feature].astype('category')

        X = meteo_df.drop(columns=['Местное время'])
        X = X[inf_columns]

        for column in target_values:
            clfs = [
                CatBoostClassifier().load_model(f"src/models/{column.replace('/', '_')}_classificator{i}.cbm", format="cbm")
                for i in range(5)]

            predict_matrix = np.array([clf.predict_proba(X) for clf in clfs]).mean(axis=0)

            timestamps.extend(meteo_df['Местное время'].tolist())
            meteostations.extend([meteostation] * 80)
            probs.extend(predict_matrix.max(axis=1))
            labels.extend(["Нет события" if value == 'False' else column
                           for value in clfs[0].classes_[predict_matrix.argmax(axis=1)]])

    submit_df = pd.DataFrame()
    submit_df['time'] = timestamps
    submit_df['meteostations'] = meteostations
    submit_df['probs'] = probs
    submit_df['labels'] = labels
    submit_df = submit_df[submit_df['labels'] != 'Нет события']
    submit_df['description'] = submit_df['labels'].map(label_to_descr)

    return edit_submit_df(submit_df)


def edit_submit_df(submit_df: pd.DataFrame):
    result_df = []
    districts = correct_MO_to_stations(dict(get_respective_weather_df_from_sql().values))
    for x, y in districts.items():
        selected_df = submit_df[submit_df["meteostations"] == y].copy()
        selected_df["district"] = x
        result_df.append(selected_df)

    return pd.concat(result_df, ignore_index=True)


def add_events_in_db():
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    engine = create_engine(DATABASE)
    db_session_maker = sessionmaker(bind=engine)
    db_session = db_session_maker()

    db_session.query(Event).delete()

    predictions_df = get_prediction()
    predicted_events = list[Event]()
    for event in predictions_df.values:
        [datetime, _, probability, event_name, description, district] = event
        predicted_events.append(Event(event=event_name, time=datetime, probability=probability, district=district, description=description))

    db_session.add_all(predicted_events)
    db_session.commit()
