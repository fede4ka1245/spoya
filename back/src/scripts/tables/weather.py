#!/usr/bin/env python3

def main(db_connection_str: str):
    import pandas as pd
    df = pd.read_csv("../../../Данные/Данные по метеостанциям.csv")

    df["time"] = pd.to_datetime(df["Местное время"], format="%d.%m.%Y %H:%M")
    df = df.drop("Местное время", axis=1)

    df.info()

    import sqlalchemy.types
    dtypes_dict = dict[str]()
    for float_column in df.select_dtypes(["float64"]).columns.values:
        dtypes_dict[float_column] = sqlalchemy.types.DECIMAL

    from sqlalchemy import create_engine
    engine = create_engine(db_connection_str)

    print("importing to database")
    df.to_sql("weather", engine, if_exists="replace", index=False, dtype=dtypes_dict)
    print("done")


if __name__ == "__main__":
    from env import DATABASE

    main(DATABASE)
