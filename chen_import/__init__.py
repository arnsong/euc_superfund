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


def import_samples():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    institution_id = find_institution_id(session, 'Dartmouth')
    dataframe = pd.read_csv('chen_import/sediment_individual.csv')
    with open('sample.json') as f:
        metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        column_metadata = copy(metadata)
        location_id = find_location_id(session, row)
        min_depth, max_depth = str(row['sample depth (cm)']).split('-') \
            if row['sample depth (cm)'] == row['sample depth (cm)'] else [None, None]
        new_sample = m.Sample(
            institution_id=institution_id,
            location_id=location_id,
            column_metadata=column_metadata,
            collection_datetime=row['sample_date'],
            file_name=nan_to_empty(row['file name for data pull']),
            sample_type=row['sample type'],
            min_depth=min_depth,
            max_depth=max_depth
        )
        session.add(new_sample)
        session.commit()


def find_location_id(session, row):
    location_id = session.query(m.Location.id).filter_by(
        site_name=nan_to_empty(row['site name']),
        site_code=nan_to_empty(row['site code']),
        state=nan_to_empty(row['state']),
        system=nan_to_empty(row['system']),
        subsite=nan_to_empty(row['subsite'])
    ).one()
    return location_id[0]


def find_institution_id(session, institution_name):
    institution_id = session.query(m.Institution.id).filter_by(name=institution_name).one()
    return institution_id[0]
