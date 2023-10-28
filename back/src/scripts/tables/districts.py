#!/usr/bin/env python3

from OSMPythonTools.element import Element

from src.tables import District


def get_possible_districts():
    from OSMPythonTools.overpass import Overpass, OverpassResult

    overpass_api = Overpass()
    districts_query_result: OverpassResult = overpass_api.query(
        "rel(56.035, 51.394, 61.867, 59.875)[boundary=administrative];out;")
    return districts_query_result.elements()


def get_osm_id(district_name: str, possible_districts: list[Element]) -> int | None:
    osm_id = None

    expanded_name: str = district_name.replace(" город", '')\
        .replace("МО", "муниципальный округ")\
        .replace("ГО", "городской округ")
    for element in possible_districts:
        if expanded_name in element.tag("name").replace('ё', 'е'):
            osm_id = element.id()
            break

    if osm_id is None:
        shortened_name: str = district_name.replace(" город", '')\
            .replace("МО", '')\
            .replace("ГО", '')\
            .strip().split()[1]
        for element in possible_districts:
            if shortened_name in element.tag("name").replace('ё', 'е'):
                osm_id = element.id()
                break

    return osm_id


def commit_districts(districts: list[District], db_connection_str: str, recreate_table: bool = True):
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    engine = create_engine(db_connection_str)
    db_session_maker = sessionmaker(bind=engine)
    db_session = db_session_maker()

    if recreate_table:
        db_session.query(District).delete()

    db_session.add_all(districts)
    db_session.commit()


def main():
    from csv import reader as csv_reader
    from requests import get

    from env import DATABASE

    possible_districts = get_possible_districts()
    if possible_districts is None:
        print("Error: can not find possible districts")
        return

    parsed_districts = list[District]()
    with open("./Данные/Данные по метеостанциям. Соответствие МО.csv") as input_table_file:
        table_reader = csv_reader(input_table_file, delimiter=',')
        table_header = next(table_reader)
        for district_name, raw_meteorology_station_name in table_reader:
            district_name, raw_meteorology_station_name = district_name.strip(), raw_meteorology_station_name.strip()

            osm_id = get_osm_id(district_name, possible_districts)

            if osm_id is None:
                print(f"Error: \"{district_name}\" was not found, skipping")
                continue

            meteorology_station_name: str = raw_meteorology_station_name \
                .replace("г. ", '').replace("п. ", '').replace("с. ", '').strip()

            geometry = get(f"https://polygons.openstreetmap.fr/get_geojson.py?id={osm_id}&params=0").json()

            parsed_districts.append(District(osm_id=osm_id, name=district_name,
                                             raw_meteorology_station_name=raw_meteorology_station_name,
                                             meteorology_station_name=meteorology_station_name, geometry=geometry))

    commit_districts(parsed_districts, DATABASE)


if __name__ == "__main__":
    main()
