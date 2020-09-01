from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Text
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
    individual_id = Column(String(20))
    latitude = Column(Numeric(10, 5))
    longitude = Column(Numeric(10, 5))
    biome = Column(String(50))
    environmental_feature = Column(String(50))


class Sample(Base):
    __tablename__ = 'samples'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    collection_datetime = Column(DateTime)
    sample_category = Column(String(20))
    file_name = Column(String(100))


class WaterSample(Base):
    __tablename__ = 'water_samples'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    tidal_cycle = Column(String(4))
    salinity = Column(Numeric(10, 5))
    temp = Column(Numeric(10, 5))
    conductivity = Column(Numeric(10, 5))
    ph = Column(Numeric(10, 5))


class SedimentSample(Base):
    __tablename__ = 'sediment_samples'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    sample_type = Column(String(20))
    percent_loi = Column(Numeric(10, 5))  # Loss on ignition


class BiotaSample(Base):
    __tablename__ = 'biota_samples'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    biota_id = Column(Integer, ForeignKey("biota.id"), nullable=False)
    wet_weight = Column(Numeric(10, 5))
    dry_weight = Column(Numeric(10, 5))
    length = Column(Integer)
    width = Column(Integer)
    notes = Column(String(50))


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    note = Column(Text)


class Biota(Base):
    __tablename__ = 'biota'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    taxonomic_group = Column(String(50))
    genus = Column(String(50))
    species = Column(String(50))
    common_name = Column(String(50))


class Compound(Base):
    __tablename__ = 'compounds'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    name = Column(String(50))


class SampleCompound(Base):
    __tablename__ = 'sample_compounds'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    compound_id = Column(Integer, ForeignKey("compounds.id"), nullable=False)
    measurement = Column(Numeric(10, 5))
    # units = Column(String(10))  # Should this be only in the metadata tags?


class QualityControl(Base):
    __tablename__ = 'quality_controls'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    dorm_percent_recovery = Column(Integer)
    tort2_percent_recovery = Column(Integer)
    analysis_dup_rpd = Column(Integer)


Base.metadata.create_all(engine)
