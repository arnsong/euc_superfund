import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_none, find_compound_ids, find_institution_id
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

    # Is this CSV day 0?
    dataframe = pd.read_csv('duke_import/mercury_analysis.csv')
    with open('sample.json') as f:
        metadata = json.load(f)
    with open('sample_compound.json') as f:
        sample_compound_metadata = json.load(f)
