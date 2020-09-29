from dataset import Dataset
from dataset import write_out_unique_locations
from copy import copy
import json
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_none, find_compound_ids, find_institution_id, insert_record


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
        create_params = {
            'site_name': nan_to_none(row['site_name']),
            'site_code': nan_to_none(row['site_code']),
            'state': nan_to_none(row['state']),
            'system': nan_to_none(row['system']),
            'subsite': nan_to_none(row['subsite']),
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'column_metadata': copy(metadata)
        }
        insert_record(session, m.Location, create_params)


def import_samples():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    institution_id = find_institution_id(session, 'Dartmouth')
    compound_ids = find_compound_ids(session)
    compound_map = {
        'mehg': ['sediment MeHg (ng/g DW)', 'mehg_units'],
        'total_hg': ['sediment THg (ng/g DW)', 'total_hg_units'],
        'percent_loi': ['%LOI', '']
    }
    dataframe = pd.read_csv('chen_import/sediment_individual.csv')
    with open('sample.json') as f:
        metadata = json.load(f)
    with open('sample_compound.json') as f:
        sample_compound_metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        location_id = find_location_id(session, row)
        min_depth, max_depth = str(row['sample depth (cm)']).split('-') \
            if row['sample depth (cm)'] == row['sample depth (cm)'] else [None, None]
        create_params = {
            'institution_id': institution_id,
            'location_id': location_id,
            'column_metadata': copy(metadata),
            'collection_datetime': row['sample_date'],
            'file_name': nan_to_none(row['file name for data pull']),
            'sample_type': row['sample type'],
            'sample_category': 'Sediment',
            'min_depth': min_depth,
            'max_depth': max_depth
        }
        new_sample = insert_record(session, m.Sample, create_params)

        for compound, measurement_array in compound_map.items():
            create_params = {
                'column_metadata': copy(sample_compound_metadata),
                'sample_id': new_sample.id,
                'compound_id': compound_ids[compound],
                'measurement': row[measurement_array[0]] if str(row[measurement_array[0]]).strip() else None,
                'units': row[measurement_array[1]] if measurement_array[1] else None
            }
            insert_record(session, m.SampleCompound, create_params)


def find_location_id(session, row):
    location_id = session.query(m.Location.id).filter_by(
        site_name=nan_to_none(row['site name']),
        site_code=nan_to_none(row['site code']),
        state=nan_to_none(row['state']),
        system=nan_to_none(row['system']),
        subsite=nan_to_none(row['subsite'])
    ).one()
    return location_id[0]
