
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text, Date, DateTime, Float, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

SegmentEnum = Enum("rail", "port", "energy", "data", "customs", name="segment_enum")
EntityTypeEnum = Enum("gov", "SOE", "private", "IFI", "NGO", "other", name="entity_type_enum")
SourceTypeEnum = Enum("gov", "IFI", "media", "think_tank", "meeting_notes", "other", name="source_type_enum")
ProjectStatusEnum = Enum("announced", "planned", "under_construction", "operational", "cancelled", name="project_status_enum")
NodeTypeEnum = Enum("person", "entity", "project", name="node_type_enum")
NodeTypeEnumTo = Enum("person", "entity", "project", name="node_type_enum_to")

JurisdictionLevelEnum = Enum("supranational", "national", "state_province", "local", name="jurisdiction_level_enum")
InstrumentTypeEnum = Enum("law", "decree", "regulation", "policy", "mou", "question", "other", name="instrument_type_enum")
InstrumentStatusEnum = Enum("draft", "proposed", "adopted", "enacted", "effective", "repealed", name="instrument_status_enum")

class Source(Base):
    __tablename__ = "sources"
    id = Column(String, primary_key=True)
    url = Column(Text, nullable=False)
    publisher = Column(Text, nullable=False)
    type = Column(SourceTypeEnum, nullable=True)
    language = Column(String(8), nullable=True)
    captured_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Entity(Base):
    __tablename__ = "entities"
    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)
    type = Column(EntityTypeEnum, nullable=False)
    country_id = Column(String(2), nullable=False)
    website = Column(Text, nullable=True)
    description = Column(Text, nullable=True)

class Person(Base):
    __tablename__ = "people"
    id = Column(String, primary_key=True)
    full_name = Column(Text, nullable=False)
    role_title = Column(Text, nullable=True)
    entity_id = Column(String, ForeignKey("entities.id"), nullable=True)
    country_id = Column(String(2), nullable=True)
    bio_short = Column(Text, nullable=True)

class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)
    segment = Column(SegmentEnum, nullable=False)
    corridor_section = Column(Text, nullable=True)
    countries_involved = Column(JSONB, nullable=True)
    status = Column(ProjectStatusEnum, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date_est = Column(Date, nullable=True)

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    entity_id = Column(String, ForeignKey("entities.id"), nullable=True)
    amount_original = Column(Float, nullable=False)
    currency = Column(String(8), nullable=False)
    amount_eur = Column(Float, nullable=True)
    amount_usd = Column(Float, nullable=True)
    date = Column(Date, nullable=False)
    purpose = Column(Text, nullable=True)
    countries_involved = Column(JSONB, nullable=True)
    segment = Column(SegmentEnum, nullable=False)
    source_id = Column(String, ForeignKey("sources.id"), nullable=False)
    original_lang = Column(String(8), nullable=True)
    summary_fr = Column(Text, nullable=True)
    summary_en = Column(Text, nullable=True)
    summary_ar = Column(Text, nullable=True)
    credibility_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Statement(Base):
    __tablename__ = "statements"
    id = Column(String, primary_key=True)
    person_id = Column(String, ForeignKey("people.id"), nullable=True)
    entity_id = Column(String, ForeignKey("entities.id"), nullable=True)
    date = Column(Date, nullable=False)
    language = Column(String(8), nullable=True)
    quote = Column(Text, nullable=False)
    summary_fr = Column(Text, nullable=True)
    summary_en = Column(Text, nullable=True)
    summary_ar = Column(Text, nullable=True)
    stance_tag = Column(JSONB, nullable=True)
    countries_involved = Column(JSONB, nullable=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=False)
    credibility_score = Column(Float, nullable=True)

class Event(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True)
    title = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    location = Column(Text, nullable=True)
    countries_involved = Column(JSONB, nullable=True)
    speakers = Column(JSONB, nullable=True)
    links = Column(JSONB, nullable=True)
    summary_fr = Column(Text, nullable=True)
    summary_en = Column(Text, nullable=True)
    summary_ar = Column(Text, nullable=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=False)
    credibility_score = Column(Float, nullable=True)

class News(Base):
    __tablename__ = "news"
    id = Column(String, primary_key=True)
    title = Column(Text, nullable=False)
    outlet = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    language = Column(String(8), nullable=True)
    summary_fr = Column(Text, nullable=True)
    summary_en = Column(Text, nullable=True)
    summary_ar = Column(Text, nullable=True)
    tags = Column(JSONB, nullable=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=False)
    credibility_score = Column(Float, nullable=True)

class Relation(Base):
    __tablename__ = "relations"
    id = Column(String, primary_key=True)
    from_type = Column(NodeTypeEnum, nullable=False)
    from_id = Column(String, nullable=False)
    to_type = Column(NodeTypeEnumTo, nullable=False)
    to_id = Column(String, nullable=False)
    relation = Column(Text, nullable=False)
    weight = Column(Float, nullable=True)

class Jurisdiction(Base):
    __tablename__ = "jurisdictions"
    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)
    country_id = Column(String(2), nullable=False)
    level = Column(JurisdictionLevelEnum, nullable=False)

class LegalInstrument(Base):
    __tablename__ = "legal_instruments"
    id = Column(String, primary_key=True)
    title = Column(Text, nullable=False)
    instrument_type = Column(InstrumentTypeEnum, nullable=False)
    number = Column(Text, nullable=True)
    status = Column(InstrumentStatusEnum, nullable=True)
    adoption_date = Column(Date, nullable=True)
    effective_date = Column(Date, nullable=True)
    country_id = Column(String(2), nullable=False)
    jurisdiction_id = Column(String, ForeignKey("jurisdictions.id"), nullable=True)
    segments = Column(JSONB, nullable=True)
    related_projects = Column(JSONB, nullable=True)
    topics = Column(JSONB, nullable=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=False)
    original_lang = Column(String(8), nullable=True)
    summary_fr = Column(Text, nullable=True)
    summary_en = Column(Text, nullable=True)
    summary_ar = Column(Text, nullable=True)
    credibility_score = Column(Float, nullable=True)
