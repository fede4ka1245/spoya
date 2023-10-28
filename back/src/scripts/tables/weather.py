#!/usr/bin/env python3

def main():
    import pandas as pd
    df = pd.read_csv("./Данные/Данные по метеостанциям.csv")

    df["time"] = pd.to_datetime(df["Местное время"], format="%d.%m.%Y %H:%M")
    df = df.drop("Местное время", axis=1)

    import sqlalchemy.types
    dtypes_dict = dict[str]()
    for float_column in df.select_dtypes(["float64"]).columns.values:
        dtypes_dict[float_column] = sqlalchemy.types.DECIMAL

    from sqlalchemy import create_engine
    from env import DATABASE

    engine = create_engine(DATABASE)

    print("importing to database", end=':')
    df.to_sql("weather", engine, if_exists="replace", index=False, dtype=dtypes_dict)
    print("done")


if __name__ == "__main__":
    main()
