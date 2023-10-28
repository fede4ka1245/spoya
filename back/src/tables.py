from dataclasses import dataclass
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@dataclass
class Event(Base):
    __tablename__ = "events"

    id: int
    id = sa.Column(sa.Integer, primary_key=True, nullable=False, autoincrement=True)

    time: datetime
    time = sa.Column(sa.DateTime, nullable=False)

    event: str
    event = sa.Column(sa.Text, nullable=False)

    probability: float
    probability = sa.Column(sa.DECIMAL, nullable=False)

    district: str
    district = sa.Column(sa.VARCHAR, nullable=False)

    description: str
    description = sa.Column(sa.Text)


@dataclass
class District(Base):
    __tablename__ = "districts"

    osm_id: int
    osm_id = sa.Column(sa.Integer, primary_key=True, nullable=False)

    name: str
    name = sa.Column(sa.VARCHAR, nullable=False)

    meteorology_station_name: str
    meteorology_station_name = sa.Column(sa.VARCHAR, nullable=False)

    raw_meteorology_station_name: str
    raw_meteorology_station_name = sa.Column(sa.VARCHAR, nullable=False)

    geometry: dict
    geometry = sa.Column(sa.JSON)