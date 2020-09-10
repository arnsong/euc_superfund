from copy import copy
import json
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
from helpers import nan_to_empty


Session = sessionmaker(bind=m.engine)
session = Session()

dataframe = pd.read_csv('locations.csv')

with open('../location.json') as f:
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
