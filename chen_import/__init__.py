from dataset import Dataset
from dataset import write_out_unique_locations
from copy import copy
import json
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_empty


def extract_locations():
    mapped_columns = {
        'location': {
            "site name": "site_name",
            "site code": "site_code"
        }
    }

    sediment = Dataset("", "chen_import/sediment_individual.csv", mapped_columns=mapped_columns)
    sediment_locations = sediment.get_locations()

    biota = Dataset("", "chen_import/biota_individual.csv", mapped_columns=mapped_columns)
    biota_locations = biota.get_locations()

    water = Dataset("", "chen_import/water_individual.csv", mapped_columns=mapped_columns)
    water_locations = water.get_locations()
    write_out_unique_locations(sediment_locations + biota_locations + water_locations,
                               file_name='chen_import/locations.csv')


def import_locations():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    dataframe = pd.read_csv('chen_import/locations.csv')

    with open('location.json') as f:
        metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        column_metadata = copy(metadata)
        new_location = m.Location(
            site_name=nan_to_empty(row['site_name']),
            site_code=nan_to_empty(row['site_code']),
            state=nan_to_empty(row['state']),
            system=nan_to_empty(row['system']),
            subsite=nan_to_empty(row['subsite']),
            latitude=row['latitude'],
            longitude=row['longitude'],
            column_metadata=column_metadata
        )
        session.add(new_location)
        session.commit()

