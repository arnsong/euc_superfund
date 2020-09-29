import models as m
from sqlalchemy.orm import sessionmaker
from helpers import find_compound_ids, find_institution_id, find_system_sample_id, find_isotope_ids, nan_to_none
import pandas as pd
from copy import copy
import json


def import_location_and_samples():
    Session = sessionmaker(bind=m.engine)
    session = Session()
    with open('location.json') as f:
        location_metadata = json.load(f)
    new_location = m.Location(
        site_name='Duke Wetland Mesocosm Facility',
        column_metadata=copy(location_metadata)
    )
    session.add(new_location)
    session.commit()
    # Is this CSV day 0?
    mercury_analysis_dataframe = pd.read_csv('duke_import/mercury_analysis.csv')
    sequential_extractions_dataframe = pd.read_csv('duke_import/sequential_extractions.csv')
    loi_dataframe = pd.read_csv('duke_import/loi.csv')
    import_sample_sheet(session, new_location.id, mercury_analysis_dataframe)
    import_sample_sheet(session, new_location.id, sequential_extractions_dataframe)
    import_sample_sheet(session, new_location.id, loi_dataframe)


def import_sample_sheet(session, location_id, dataframe):
    institution_id = find_institution_id(session, 'Duke')
    compound_ids = find_compound_ids(session)
    isotope_ids = find_isotope_ids(session)
    compound_map = {
        'TotHg': 'total_hg',
        'MeHg': 'mehg',
        'LOI': 'percent_loi'
    }

    with open('sample.json') as f:
        metadata = json.load(f)
    with open('sample_compound.json') as f:
        sample_compound_metadata = json.load(f)

    for idx, row in dataframe.iterrows():

        sample = find_system_sample_id(
            session,
            {'institution_id': institution_id, 'box_number': row['Box #'], 'box_zone': row['Box Zone'],
             'replicate_number': row['Sample Replicate Number']}
        )
        # Insert sample
        if not sample:
            depth = row['Depth interval (in cm)']
            min_depth, max_depth = str(depth).split('-') \
                if depth == depth and '-' in depth else [None, None]
            sample = m.Sample(
                institution_id=institution_id,
                location_id=location_id,
                column_metadata=copy(metadata),
                collection_datetime=nan_to_none(row['Sampling date']),
                min_depth=min_depth,
                max_depth=max_depth,
                sample_category='Sediment',
                box_number=row['Box #'],
                box_zone=row['Box Zone'],
                replicate_number=row['Sample Replicate Number']
            )
            session.add(sample)
            session.commit()

        if row['Analyte'] in compound_map.keys():
            if row['Analyte'] == 'LOI':
                create_params = {
                    'column_metadata': copy(sample_compound_metadata),
                    'sample_id': sample.id,
                    'compound_id': compound_ids[compound_map[row['Analyte']]],
                    'measurement': row['Value'],
                    'units': row['Analyte Units'],
                    'days_post_dosing': row['Days post-dosing']
                }
                new_sample_compound = m.SampleCompound(**create_params)
                session.add(new_sample_compound)
                session.commit()

            else:
                for isotope, isotope_id in isotope_ids.items():
                    if isotope in row:
                        create_params = {
                            'column_metadata': copy(sample_compound_metadata),
                            'sample_id': sample.id,
                            'compound_id': compound_ids[compound_map[row['Analyte']]],
                            'measurement': None if row[isotope] == 'BDL' else row[isotope],
                            'units': row['Analyte Units'],
                            'source_of_hg_spike_id': isotope_id,
                            'days_post_dosing': row['Days post-dosing']
                        }
                        new_sample_compound = m.SampleCompound(**create_params)
                        session.add(new_sample_compound)
                        session.commit()
