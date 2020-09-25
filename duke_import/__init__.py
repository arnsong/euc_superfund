import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_none, find_compound_ids, find_institution_id, find_system_sample_id
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

    institution_id = find_institution_id(session, 'Duke')
    compound_ids = find_compound_ids(session)
    compound_map = {
        'TotHg': 'total_hg',
        'MeHg': 'mehg'
    }

    # Is this CSV day 0?
    dataframe = pd.read_csv('duke_import/mercury_analysis.csv')
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
            print('Trying to parse: {}'.format(row['Depth interval (in cm)']))
            depth = row['Depth interval (in cm)']
            min_depth, max_depth = str(depth).split('-') \
                if depth == depth and '-' in depth else [None, None]
            sample = m.Sample(
                institution_id=institution_id,
                location_id=new_location.id,
                column_metadata=copy(metadata),
                min_depth=min_depth,
                max_depth=max_depth,
                sample_category='Sediment',
                box_number=row['Box #'],
                box_zone=row['Box Zone'],
                replicate_number=row['Sample Replicate Number']
            )
            session.add(sample)
            session.commit()
