import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_none, find_compound_ids, find_institution_id
import pandas as pd
from copy import copy
import json


def import_samples():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    institution_id = find_institution_id(session, 'Duke')
    compound_ids = find_compound_ids(session)

    dataframe = pd.read_csv('chen_import/sediment_individual.csv')
    with open('sample.json') as f:
        metadata = json.load(f)
    with open('sample_compound.json') as f:
        sample_compound_metadata = json.load(f)
