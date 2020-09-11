import chen_import
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
import config


def import_institutions():
    Session = sessionmaker(bind=m.engine)
    session = Session()

    path = config.PATH_TO_INSTITUTIONS

    dataframe = pd.read_csv(path)

    for idx, row in dataframe.iterrows():
        new_institution = m.Institution(name=row['name'])
        session.add(new_institution)
        session.commit()


def main():
    m.Base.metadata.create_all(m.engine)
    import_institutions()
    chen_import.extract_locations()
    chen_import.import_locations()


if __name__ == "__main__":
    main()
