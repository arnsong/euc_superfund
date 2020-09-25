from dataset import Dataset
from dataset import write_out_unique_locations
from copy import copy
import json
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_none, find_institution_id, find_compound_ids, find_system_sample_id


def extract_locations():
    mapped_columns = {
        'location':  {
            'SITE': 'site_name'
        }
    }

    plot_mapped_columns = {
        'location':  {
            'SITE_NAME': 'site_name'
        }
    }
    marsh = Dataset("", "smithsonian_import/chesapeake_marsh.csv", mapped_columns=mapped_columns)
    marsh_locations = marsh.get_locations()

    plot = Dataset("", "smithsonian_import/chesapeake_plot.csv", mapped_columns=plot_mapped_columns)
    plot_locations = plot.get_locations()
    write_out_unique_locations(marsh_locations + plot_locations, file_name='smithsonian_import/locations.csv')


def import_locations():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    dataframe = pd.read_csv('smithsonian_import/locations.csv')

    with open('location.json') as f:
        metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        new_location = m.Location(
            site_name=nan_to_none(row['site_name']),
            column_metadata=copy(metadata)
        )
        session.add(new_location)
        session.commit()


def import_samples():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    institution_id = find_institution_id(session, 'Smithsonian')
    compound_ids = find_compound_ids(session)
    measurement_params_map = {
        'MeHg-bulk': 'mehg',
        'THg-bulk': 'total_hg',
        'LOI': 'percent_loi'
    }

    dataframe = pd.read_csv('smithsonian_import/chesapeake_marsh.csv')
    with open('sample.json') as f:
        metadata = json.load(f)
    with open('sample_compound.json') as f:
        sample_compound_metadata = json.load(f)
    with open('sample_preparation.json') as f:
        sample_preparation_metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        if row['SAMPLE TYPE'] != 'Soil':
            continue
        sample = find_system_sample_id(
            session,
            {'institution_id': institution_id, 'lab_sample_id': row['LAB SAMPLE ID']}
        )
        # Insert sample
        if not sample:
            location_id = find_location_id(session, row)
            depth = row['Core Depth']
            min_depth, max_depth = str(depth).split(' ')[0].split('-') \
                if depth == depth and '-' in depth else [None, None]
            sample = m.Sample(
                institution_id=institution_id,
                location_id=location_id,
                column_metadata=copy(metadata),
                lab_sample_id=row['LAB SAMPLE ID'],
                collection_datetime=row['COLLECTION_DATE'],
                file_name=row['SOURCE FILE'],
                min_depth=min_depth,
                max_depth=max_depth,
                average_depth=nan_to_none(row['Ave Core depth (cm)']),
                sample_type=row['SAMPLE TYPE'],
                sample_category='Sediment'
            )
            session.add(sample)
            session.commit()

        if row['PARAMETER'] in measurement_params_map.keys():
            # Insert Sample prep
            new_sample_preparation = m.SamplePreparation(
                column_metadata=copy(sample_preparation_metadata),
                sample_id=sample.id,
                analysis_date=row['ANALYSIS DATE'],
                method=row['SAMPLING METHOD'],
                filter=row['FILTER'],
                preservation=nan_to_none(row['SAMPLE PRESERVATION']),
                detection_limit=nan_to_none(row['DL']),
                detection_limit_units=row['UNITS'],
                detection_limit_flag=nan_to_none(row['DL Flag']),
                dilution=nan_to_none(row['Dilution'])
            )
            session.add(new_sample_preparation)
            session.commit()

            # Insert Sample measurements
            new_sample_compound = m.SampleCompound(
                column_metadata=copy(sample_compound_metadata),
                sample_id=sample.id,
                compound_id=compound_ids[measurement_params_map[row['PARAMETER']]],
                measurement=row['VALUE'],
                units=row['UNITS']
            )
            session.add(new_sample_compound)
            session.commit()


def find_location_id(session, row):
    return session.query(m.Location.id).filter_by(site_name=nan_to_none(row['SITE'])).one()[0]
