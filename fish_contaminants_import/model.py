import config

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

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
    STATE = Column(String(14))

    WATERBODY_NAME = Column(String(35))
    LATITUDE = Column(Float)
    LONGITUDE = Column(Float)
    MAP_DATUM = Column(String(12))
    SITE_TYPE = Column(String(30))
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
    COMMON_NAME = Column(String(40))
    TOTAL_LENGTH = Column(Integer)
    TOTAL_LENGTH_UNITS = Column(String(22))
    COMPOSITE = Column(String(3))
    PRED_OR_BD = Column(String(20))
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
    TISSUE_TYPE = Column(String(40))
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
    SITE_ID = Column(String(20), ForeignKey('sites.SITE_ID'))
    
    SOURCE = Column(String(50))
    
    site = relationship("Site")

engine = create_engine(
    f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}", echo=False
)

Base.metadata.create_all(engine)
