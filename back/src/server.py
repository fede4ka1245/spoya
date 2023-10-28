from flask import Flask, request, jsonify

from flask_cors import CORS

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

from src.tables import Event, Base, District

from env import DATABASE


app = Flask(__name__)
CORS(app)

engine = create_engine(DATABASE)
db_session_maker = sessionmaker(bind=engine)
db_session = db_session_maker()

Base.metadata.create_all(engine)


@app.get("/get-events")
def get_events():
    date = request.args.get("date")
    if date is None:
        return "Error: date is not specified"

    try:
        date = datetime.strptime(date, "%d.%m.%Y").date()
    except ValueError:
        return "Error: date is not correct"

    type = request.args.get("type")
    if type is None:
        return "Error: "

    result = dict[str, Event]()
    day_events_amounts = dict[str, int]()
    for event in db_session.query(Event).filter((func.DATE(Event.time) == date) & (Event.event == type)).all():
        if event.district in result:
            result[event.district].probability += event.probability
            day_events_amounts[event.district] += 1
        else:
            result[event.district] = event
            day_events_amounts[event.district] = 1

    for district in result.keys():
        result[district].probability /= day_events_amounts.get(district, 1)

    return jsonify(result)


@app.get("/get-districts")
def get_districts():
    return jsonify(db_session.query(District).all())


@app.get("/get-events-types")
def get_events_types():
    events_types = set[str](map(lambda query_result_row: query_result_row[0], db_session.query(Event.event).distinct().all()))
    return jsonify(list(events_types))


@app.get("/get-latest-dates")
def get_latest_dates():
    days_amount = 10

    result = list[str]()
    latest_date: datetime = db_session.query(func.max(Event.time)).first()[0]
    for _ in range(days_amount):
        result.append(latest_date.strftime("%d.%m.%Y"))
        latest_date -= timedelta(days=1)
    return jsonify(result)


if __name__ == "__main__":
    app.run()
