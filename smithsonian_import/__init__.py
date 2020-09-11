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
        'location':  {
            "SITE": "site_name"
        }
    }

    plot_mapped_columns = {
        'location':  {
            "SITE_NAME": "site_name"
        }
    }
    marsh = Dataset("", "smithsonian_import/chesapeake_marsh.csv", mapped_columns=mapped_columns)
    marsh_locations = marsh.get_locations()

    plot = Dataset("", "smithsonian_import/chesapeake_plot.csv", mapped_columns=plot_mapped_columns)
    plot_locations = plot.get_locations()
    write_out_unique_locations(marsh_locations + plot_locations)


def import_locations():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    dataframe = pd.read_csv('smithsonian_import/locations.csv')

    with open('location.json') as f:
        metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        column_metadata = copy(metadata)
        new_location = m.Location(
            site_name=nan_to_empty(row['site_name']),
            column_metadata=column_metadata
        )
        session.add(new_location)
        session.commit()
