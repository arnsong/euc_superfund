from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, DateTime
from sqlalchemy.dialects.postgresql import JSONB
import config

engine = create_engine(
    f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}", echo=True
)
Base = declarative_base()


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    site_name = Column(String(50))
    site_code = Column(String(5))
    state = Column(String(2))
    system = Column(String(50))
    subsite = Column(String(3))
    latitude = Column(Numeric(10, 5))
    longitude = Column(Numeric(10, 5))
    biome = Column(String(50))
    environmental_feature = Column(String(50))


class Sample(Base):
    __tablename__ = 'samples'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    collection_datetime = Column(DateTime)
    sample_type = Column(String(20))


class Compound(Base):
    __tablename__ = 'compounds'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    name = Column(String(10))


class SampleCompound(Base):
    __tablename__ = 'sample_compounds'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    measurement = Column(Numeric(10, 5))
    units = Column(String(10))


Base.metadata.create_all(engine)
