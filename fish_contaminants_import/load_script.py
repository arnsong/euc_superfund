import config

import yaml
import pandas as pd
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, Numeric, ForeignKey

engine = create_engine(
    f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}", echo=False
)

Base = declarative_base()

class Site(Base):
    __tablename__ = 'sites'

    SITE_ID = Column(String(20), primary_key=True, nullable=False)

    UID = Column(Integer)
    EPA_REGION = Column(String(10))
    NCCR_REGION = Column(String(12))
    NCA_REGION = Column(String(12))
    NEP_NAME = Column(String(20))
    NPS_PARK = Column(String(4))
    COUNTRY = Column(String(3))
    PROVINCE = Column(String(20))
    STATE = Column(String(2))

    WATERBODY_NAME = Column(String(30))
    LATITUDE = Column(Float)
    LONGITUDE = Column(Float)
    MAP_DATUM = Column(String(12))
    SITE_TYPE = Column(String(12))
    STREAM_ORDER = Column(Integer)
    DSNTYPE = Column(String(5))
    MDCATY = Column(String(41))
    PANEL = Column(String(8))
    STATUS10 = Column(String(15))
    STRATUM = Column(String(29))
    TNT = Column(String(15))
    WGT_CAT = Column(String(36))
    WGT_NCCA10 = Column(String(11))
    RSRC_CLASS = Column(String(22))
    COMMENTS = Column(String(100))
    
    SOURCE = Column(String(50))
    
    def __repr__(self):
        return f"<Site(SITE_ID={self.SITE_ID})"
    
class Sample(Base):
    __tablename__ = 'samples'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    UID = Column(Integer)
    EPA_SAMPLE_ID = Column(Integer)
    SPECIMEN_ID = Column(Numeric(7,1))
    SPECIMEN_SORT = Column(Integer)
    VISIT_NO = Column(Integer)
    COLLECTION_DATE = Column(DateTime)
    STATION_DEPTH = Column(Float)
    STATION_DEPTH_UNITS = Column(String(1))
    SITE_SAMPLED = Column(String(1))
    INDEX_VISIT = Column(String(1))
    BATCH_ID = Column(String(22))
    SAMPLE_ID = Column(Integer)
    LAB_SAMPLE_ID = Column(Integer)
    FAMILY = Column(String(13))
    TAXA_NAME = Column(String(34))
    COMMON_NAME = Column(String(21))
    TOTAL_LENGTH = Column(Integer)
    TOTAL_LENGTH_UNITS = Column(String(22))
    COMPOSITE = Column(String(3))
    PRED_OR_BD = Column(String(2))
    COMPOSITE_CLASS = Column(String(11))
    DEVIATION = Column(String(16))
    PARAMETER = Column(String(10))
    PARAMETER_NAME = Column(String(20))
    PARAMETER_CATEGORY = Column(String(10))
    CAS_NO = Column(String(10))
    VALUE = Column(Float)
    UNITS = Column(String(10))
    BATCH_ID = Column(String(22))
    MDL = Column(Float)
    RL = Column(Float)
    DATE_ANALYZED = Column(DateTime)
    HOLDING_TIME = Column(Integer)
    METHOD = Column(String(10))
    QA_CODES = Column(String(21))
    FILLET_PREP = Column(String(255))
    TISSUE_TYPE = Column(String(14))
    PERCENT_LIPIDS = Column(Float)
    DATE_ANALYZED = Column(DateTime)
    HOLDING_TIME = Column(Integer)
    PARAMETER = Column(String(9))
    PARAMETER_NAME = Column(String(43))
    CAS_NO = Column(String(10))
    PARAMETER_CATEGORY = Column(String(10))
    AMOUNT = Column(Float)
    AMOUNT_UNITS = Column(String(12))
    MDL = Column(Float)
    METHOD = Column(String(14))
    QL = Column(Float)
    RL = Column(Float)
    QA_CODES = Column(String(21))
    COMMENTS = Column(String(200))

    SOURCE = Column(String(50))

    SITE_ID = Column(String(20), ForeignKey('sites.SITE_ID'))
    site = relationship("Site")

Base.metadata.create_all(engine)


##### Load data load config

def load_database(config_file, engine=None, if_exists='append', index=False):

    if not engine:
        print("A sqlalchemy engine is required")
        return

    # Start session for queries
    Session = sessionmaker(bind=engine)
    session = Session()

    # TODO -- check if table exists
    
    mapping = yaml.load(open(config_file), Loader=yaml.FullLoader)

    # TODO -- After loading mapping, make sure that the columns exist, if not add them to the table
    
    # Load csv data into pandas dataframe
    if mapping['Type'] == 'xlsx':
        data = pd.read_excel(mapping['Filename'], mapping['Sheet'])
    else:
        data = pd.read_csv(mapping['Filename'])

        
    for table in mapping['tables']:
        
        # Load csv data into pandas dataframe
        if mapping['Type'] == 'xlsx':
            data = pd.read_excel(mapping['Filename'], mapping['Sheet'])
        else:
            data = pd.read_csv(mapping['Filename'])
        
        columns = mapping['tables'][table]['columns']
        
        # Rename column headings
        for column_name in columns.keys():
            data.rename(columns={columns[column_name]: column_name}, inplace=True)

        drop_cols = [ col_name for col_name in data.columns if col_name not in columns.keys() ]
        data.drop(columns=drop_cols, inplace=True)

        for idx, row in data.iterrows():
            obj = mapping['tables'][table]['sqlalchemy_obj']
            keys = mapping['tables'][table]['keys']

            eval_string = f"session.query({obj})"

            for key in keys:
                value = row[key]
                eval_string += f'.filter({obj}.{key}=="{value}")'

            eval_string += ".all()"
            query_results = eval(eval_string)

            if len(query_results)==0:
                # Add row with table specific columns to table
                pd.DataFrame(row).T.to_sql(table, con=engine, if_exists='append', index=False)
            else:
                # Update fields
                for result in query_results: 
                    for col in data.columns:
                        if col=='STREAM_ORDER':
                            if row[col]=='8+':
                                row[col] = '8'
                        value = row[col]
                        exec(f'result.{col}="{value}"')

            if idx%100==0:
                print(f"Index: {idx}/{len(data.index)}")
        
        print(f"{table} is finished")

config_files = sys.argv[1:]

for config in config_files:
    load_database(config, engine)
