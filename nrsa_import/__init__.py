from dataset import Dataset
from copy import copy
import json
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_empty


def extract_locations():
    mapped_columns = {
        'location':  {
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Site.Type": "urban",
            "State": "state",
            "site_id": "site_name"
        }
    }

    nrsa = Dataset("", "nrsa_import/nrsa.csv", mapped_columns=mapped_columns)
    nrsa.get_locations(to_file="nrsa_import/locations.csv")


def import_locations():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    dataframe = pd.read_csv('nrsa_import/locations.csv')

    with open('location.json') as f:
        metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        column_metadata = copy(metadata)
        new_location = m.Location(
            site_name=nan_to_empty(row['site_name']),
            latitude=row['latitude'],
            longitude=row['longitude'],
            urban=(row['urban'] == 'Urban'),
            state=nan_to_empty(row['state']),
            column_metadata=column_metadata
        )
        session.add(new_location)
        session.commit()
