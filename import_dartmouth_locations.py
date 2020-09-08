from copy import copy
import json
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
import config
from helpers import nan_to_empty


Session = sessionmaker(bind=m.engine)
session = Session()

path = config.PATH_TO_DARTMOUTH_LOCATIONS

dataframe = pd.read_csv(path)

with open('chen_import/location.json') as f:
    metadata = json.load(f)

for idx, row in dataframe.iterrows():
    column_metadata = copy(metadata)
    new_location = m.Location(
        site_name=nan_to_empty(row['site name']),
        site_code=nan_to_empty(row['site code']),
        state=nan_to_empty(row['state']),
        system=nan_to_empty(row['system']),
        subsite=nan_to_empty(row['subsite']),
        latitude=row['latitude'],
        longitude=row['longitude'],
        column_metadata=column_metadata
    )
    session.add(new_location)
    session.commit()
