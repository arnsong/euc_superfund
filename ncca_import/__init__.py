from dataset import Dataset
from copy import copy
import json
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_none


def extract_locations():
    mapped_columns = {
        'location':  {
            "station": "site_name",
            "stat_alt": "site_code"
        }
    }

    ncca = Dataset("", "ncca_import/ncca.csv", mapped_columns=mapped_columns)
    ncca.get_locations(to_file="ncca_import/locations.csv")


def import_locations():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    dataframe = pd.read_csv('ncca_import/locations.csv')

    with open('location.json') as f:
        metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        column_metadata = copy(metadata)
        new_location = m.Location(
            site_name=nan_to_none(row['site_name']),
            site_code=nan_to_none(row['site_code']),
            column_metadata=column_metadata
        )
        session.add(new_location)
        session.commit()
