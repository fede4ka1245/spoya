#!/usr/bin/env python3

from argparse import ArgumentParser

from src.scripts.tables.districts import main as add_districts_in_db
from src.scripts.prediction.danger_prediction import add_events_in_db
from src.server import app

if __name__ == "__main__":
    argument_parser = ArgumentParser()

    argument_parser.add_argument("-r", "--run", action="store_true")
    argument_parser.add_argument("-p", "--predict", action="store_true")
    argument_parser.add_argument("-d", "--districts", action="store_true")

    arguments = argument_parser.parse_args()

    if arguments.districts:
        add_districts_in_db()
    if arguments.predict:
        add_events_in_db()
    if arguments.run or not (arguments.districts or arguments.predict or arguments.run):
        app.run()
