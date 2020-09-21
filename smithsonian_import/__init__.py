from dataset import Dataset
from dataset import write_out_unique_locations
from copy import copy
import json
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_empty, find_institution_id, find_compound_ids


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
    write_out_unique_locations(marsh_locations + plot_locations, file_name='smithsonian_import/locations.csv')


def import_locations():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    dataframe = pd.read_csv('smithsonian_import/locations.csv')

    with open('location.json') as f:
        metadata = json.load(f)

    for idx, row in dataframe.iterrows():
        new_location = m.Location(
            site_name=nan_to_empty(row['site_name']),
            column_metadata=copy(metadata)
        )
        session.add(new_location)
        session.commit()


def import_samples():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    institution_id = find_institution_id(session, 'Smithsonian')
    compound_ids = find_compound_ids(session)

    dataframe = pd.read_csv('smithsonian_import/chesapeake_marsh.csv')
    with open('sample.json') as f:
        metadata = json.load(f)
    with open('sample_compound.json') as f:
        sample_compound_metadata = json.load(f)
    column_metadata = copy(metadata)

    for idx, row in dataframe.iterrows():
        location_id = find_location_id(session, row)
        depth = row['Core Depth']
        min_depth, max_depth = str(depth).split(' ')[0].split('-') \
            if depth == depth and '-' in depth else [None, None]
        new_sample = m.Sample(
            institution_id=institution_id,
            location_id=location_id,
            column_metadata=column_metadata,
            lab_sample_id=row['LAB SAMPLE ID'],
            collection_datetime=row['COLLECTION_DATE'],
            file_name=row['SOURCE FILE'],
            min_depth=min_depth,
            max_depth=max_depth,
            average_depth=nan_to_empty(row['Ave Core depth (cm)'])
        )
        session.add(new_sample)
        session.commit()

        # for compound, measurement_array in compound_map.items():
        #     new_sample_compound = m.SampleCompound(
        #         column_metadata=copy(sample_compound_metadata),
        #         sample_id=new_sample.id,
        #         compound_id=compound_ids[compound],
        #         measurement=row[measurement_array[0]] if str(row[measurement_array[0]]).strip() else None,
        #         units=row[measurement_array[1]] if measurement_array[1] else None
        #     )
        #     session.add(new_sample_compound)
        #     session.commit()


def find_location_id(session, row):
    return session.query(m.Location.id).filter_by(site_name=nan_to_empty(row['SITE'])).one()[0]

