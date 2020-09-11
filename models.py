from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Text, Date, Boolean, Enum
from sqlalchemy.dialects.postgresql import JSONB
import config
import enum

engine = create_engine(
    f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}", echo=True
)
Base = declarative_base()


class FoodChain(enum.Enum):
    predator = 1
    bottom_feeder = 2


# To keep track of which center samples came from
class Institution(Base):
    __tablename__ = 'institutions'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50))


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    site_name = Column(String(50))
    site_code = Column(String(5))
    site_id = Column(String(20))
    city = Column(String(50))
    county = Column(String(50))
    county_code = Column(String(50))
    state = Column(String(2))
    system = Column(String(50))
    subsite = Column(String(50))
    individual_id = Column(String(20))
    latitude = Column(Numeric(10, 5))
    longitude = Column(Numeric(10, 5))
    biome = Column(String(50))
    environmental_feature = Column(String(50))
    urban = Column(Boolean)


class Sample(Base):
    __tablename__ = 'samples'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    lab_sample_id = Column(String(50))
    specimen_id = Column(String(10))
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
    min_depth = Column(Integer)
    max_depth = Column(Integer)
    average_depth = Column(Integer)
    percent_loi = Column(Numeric(10, 5))  # Loss on ignition


class BiotaSample(Base):
    __tablename__ = 'biota_samples'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    biota_id = Column(Integer, ForeignKey("biota.id"), nullable=False)
    tissue_type = Column(String(10))
    wet_weight = Column(Numeric(10, 5))
    dry_weight = Column(Numeric(10, 5))
    length = Column(Integer)
    width = Column(Integer)
    age = Column(Integer)
    percent_lipids = Column(Numeric(10, 5))
    notes = Column(String(50))


class SamplePreparation(Base):
    __tablename__ = 'sample_preparations'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    analysis_date = Column(Date)
    method = Column(String(50))
    filter = Column(String(50))
    preservation = Column(String(50))
    detection_limit = Column(Numeric(10, 5))
    detection_limit_flag = Column(String(1))
    dilution = Column(Integer)


class ExperimentType(Base):
    __tablename__ = 'experiment_types'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    experiment_type = Column(String(50))


class ExperimentSample(Base):
    __tablename__ = 'experiment_samples'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    experiment_type_id = Column(Integer, ForeignKey("experiment_types.id"), nullable=False)
    block = Column(Integer)
    runner = Column(String(50))
    length_of_exposure = Column(Integer)
    treatment = Column(String(50))
    treatment_class = Column(String(50))
    treatment_number = Column(String(50))
    plot = Column(String(50))
    detection_limit = Column(Numeric(10, 5))
    detection_limit_flag = Column(String(1))
    min_depth = Column(Integer)  # Should this have a SedimentSample record instead?
    max_depth = Column(Integer)  # Should this have a SedimentSample record instead?
    comment = Column(Text)


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
    family = Column(String(50))
    species = Column(String(50))
    scientific_name = Column(String(50))
    common_name = Column(String(50))
    food_chain = Column(Enum(FoodChain))
    sort = Column(Integer)


class Compound(Base):
    __tablename__ = 'compounds'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    name = Column(String(50))


class CompoundAnalyticGroup(Base):
    __tablename__ = 'compound_analytic_groups'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    compound_id = Column(Integer, ForeignKey("compounds.id"), nullable=False)
    group = Column(String(50))
    units = Column(String(50))
    description = Column(String(50))
    reference = Column(String(50))


class SampleCompound(Base):
    __tablename__ = 'sample_compounds'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    compound_id = Column(Integer, ForeignKey("compounds.id"), nullable=False)
    measurement = Column(Numeric(10, 5))
    qa_flag = Column(String(10))
    # units = Column(String(10))  # Should this be only in the metadata tags?


class QualityControl(Base):
    __tablename__ = 'quality_controls'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    column_metadata = Column(JSONB, nullable=False)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    dorm_percent_recovery = Column(Integer)
    tort2_percent_recovery = Column(Integer)
    id_percent_recovery = Column(Integer)
    analysis_dup_rpd = Column(Integer)
    comment = Column(Text)

