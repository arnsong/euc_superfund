import chen_import
import smithsonian_import
import duke_import
# import ncca_import
# import nrsa_import
# import bu_import
import pandas as pd
import models as m
from sqlalchemy.orm import sessionmaker
import config

basic_metadata = {'keys': ['name'], 'tags': [None]}


def import_simple(model, path_to_input, metadata=False):
    Session = sessionmaker(bind=m.engine)
    session = Session()

    dataframe = pd.read_csv(path_to_input)

    for idx, row in dataframe.iterrows():
        create_params = {'name': row['name']}
        if metadata:
            create_params['column_metadata'] = basic_metadata
        new_record = model(**create_params)
        session.add(new_record)
        session.commit()


def initialize_tables():
    m.Base.metadata.drop_all(m.engine)
    m.Base.metadata.create_all(m.engine)


def import_all_locations():
    chen_import.extract_locations()
    chen_import.import_locations()
    smithsonian_import.extract_locations()
    smithsonian_import.import_locations()
    # ncca_import.extract_locations()
    # ncca_import.import_locations()
    # nrsa_import.extract_locations()
    # nrsa_import.import_locations()
    # bu_import.extract_locations()
    # bu_import.import_locations()


def main():
    initialize_tables()
    import_simple(m.Institution, config.PATH_TO_INSTITUTIONS)
    import_simple(m.Compound, config.PATH_TO_COMPOUNDS, metadata=True)
    import_simple(m.Isotope, config.PATH_TO_ISOTOPES, metadata=True)
    import_all_locations()
    chen_import.import_samples()
    smithsonian_import.import_samples()
    duke_import.import_location_and_samples()

if __name__ == "__main__":
    main()
