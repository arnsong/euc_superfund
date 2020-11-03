from dataset import Dataset
from copy import copy
import json
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_none


def extract_locations():
    extract_nbh_locations()
    extract_sweden_locations()


def import_locations():
    import_nbh_locations()
    import_sweden_locations()


def extract_nbh_locations():
    mapped_columns = {
        'location':  {
            "station": "site_name",
            "AOC_name": "subsite",
        }
    }

    nbh = Dataset("", "bu_import/NBHFishTissueData_2003-2016.csv", mapped_columns=mapped_columns)
    nbh.get_locations(to_file="bu_import/nbh_locations.csv")


def extract_sweden_locations():
    sweden_mapped_columns = {
        'location': {
            "Station": "site_name",
            "Stat_Id": "site_id",
            "Longitude": "longitude",
            "Latitude": "latitude",
            "Kommun": "city",
            "county code": "county_code"
        }
    }

    sweden = Dataset("", "bu_import/sweden_data.csv", mapped_columns=sweden_mapped_columns)
    sweden.get_locations(to_file="bu_import/sweden_locations.csv")


def import_nbh_locations():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    dataframe = pd.read_csv('bu_import/nbh_locations.csv')

    with open('location.json') as f:
        metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        column_metadata = copy(metadata)
        new_location = m.Location(
            site_name=nan_to_none(row['site_name']),
            subsite=nan_to_none(row['subsite']),
            column_metadata=column_metadata
        )
        session.add(new_location)
        session.commit()


def import_sweden_locations():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    dataframe = pd.read_csv('bu_import/sweden_locations.csv')

    with open('location.json') as f:
        metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        column_metadata = copy(metadata)
        new_location = m.Location(
            site_name=nan_to_none(row['site_name']),
            site_id=nan_to_none(row['site_id']),
            latitude=row['latitude'],
            longitude=row['longitude'],
            city=nan_to_none(row['city']),
            county_code=nan_to_none(row['county_code']),
            column_metadata=column_metadata
        )
        session.add(new_location)
        session.commit()

def import_samples():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    dataframe = pd.read_csv('bu_import/NBHFishTissueData_2003-2016.csv')
    dataframe.to_sql('nbh_fish_tissue', con=m.engine)

    dataframe = pd.read_csv('bu_import/sweden_data.csv')
    dataframe.to_sql('sweden_data', con=m.engine)