from copy import copy
import json
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
import config


Session = sessionmaker(bind=m.engine)
session = Session()

path = config.PATH_TO_DARTMOUTH_LOCATIONS

dataframe = pd.read_csv(path)

with open('chen_import/location.json') as f:
    metadata = json.load(f)

for idx, row in dataframe.iterrows():
    column_metadata = copy(metadata)
    new_location = m.Location(
        site_name=row['site name'],
        site_code=row['site code'],
        state=row['state'],
        system=row['system'],
        subsite=row['subsite'],
        latitude=row['latitude'],
        longitude=row['longitude'],
        column_metadata=column_metadata
    )
    session.add(new_location)
    session.commit()
