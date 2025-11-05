
import os
from fastapi import FastAPI, Query, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Optional, List
from models import Base, Budget, Project, Statement, Event, News, Entity, Person, LegalInstrument, Jurisdiction

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/imec")
API_KEY = os.getenv("API_KEY", "changeme")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

engine = create_engine(DATABASE_URL, echo=False, future=True)

app = FastAPI(title="IMEC Intelligence Hub API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine, checkfirst=True)

def to_dict(row):
    d = {}
    for c in row.__table__.columns:
        d[c.name] = getattr(row, c.name)
    return d

def require_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True

@app.get("/budgets")
def list_budgets(country: Optional[str] = Query(None), segment: Optional[str] = Query(None), after: Optional[str] = Query(None), before: Optional[str] = Query(None), limit: int = 50):
    with Session(engine) as s:
        q = s.query(Budget).order_by(Budget.date.desc()).limit(limit)
        if country:
            q = q.filter(Budget.countries_involved.cast(str).like(f"%{country}%"))
        if segment:
            q = q.filter(Budget.segment == segment)
        if after:
            q = q.filter(Budget.date >= after)
        if before:
            q = q.filter(Budget.date < before)
        items = [to_dict(b) for b in q.all()]
        return {"items": items}

@app.get("/legal")
def list_legal(country: Optional[str] = Query(None), instrument_type: Optional[str] = Query(None), after: Optional[str] = Query(None), before: Optional[str] = Query(None), limit: int = 50):
    with Session(engine) as s:
        q = s.query(LegalInstrument).order_by(LegalInstrument.adoption_date.desc().nullslast()).limit(limit)
        if country:
            q = q.filter(LegalInstrument.country_id == country)
        if instrument_type:
            q = q.filter(LegalInstrument.instrument_type == instrument_type)
        if after:
            q = q.filter(LegalInstrument.adoption_date >= after)
        if before:
            q = q.filter(LegalInstrument.adoption_date < before)
        items = [to_dict(x) for x in q.all()]
        return {"items": items}

@app.get("/search")
def search(q: Optional[str] = None, type: Optional[List[str]] = Query(None)):
    with Session(engine) as s:
        out = []
        if (not type) or ("budgets" in type):
            out += [ {"type": "budget", **to_dict(x)} for x in s.query(Budget).order_by(Budget.date.desc()).limit(10) ]
        if (not type) or ("news" in type):
            out += [ {"type": "news", **to_dict(x)} for x in s.query(News).order_by(News.date.desc()).limit(10) ]
        if (not type) or ("legal" in type):
            out += [ {"type": "legal", **to_dict(x)} for x in s.query(LegalInstrument).order_by(LegalInstrument.adoption_date.desc()).limit(10) ]
        return {"items": out}

class BudgetIn(BaseModel):
    id: str
    amount_original: float
    currency: str
    date: str
    segment: str
    countries_involved: list[str] = []
    project_id: str | None = None
    entity_id: str | None = None
    amount_eur: float | None = None
    amount_usd: float | None = None
    purpose: str | None = None
    source_id: str
    original_lang: str | None = None
    summary_fr: str | None = None
    summary_en: str | None = None
    summary_ar: str | None = None
    credibility_score: float | None = None

@app.post("/budgets", dependencies=[Depends(require_api_key)])
def create_budget(payload: BudgetIn):
    with Session(engine) as s:
        b = Budget(
            id=payload.id,
            project_id=payload.project_id,
            entity_id=payload.entity_id,
            amount_original=payload.amount_original,
            currency=payload.currency,
            amount_eur=payload.amount_eur,
            amount_usd=payload.amount_usd,
            date=payload.date,
            purpose=payload.purpose,
            countries_involved=payload.countries_involved,
            segment=payload.segment,
            source_id=payload.source_id,
            original_lang=payload.original_lang,
            summary_fr=payload.summary_fr,
            summary_en=payload.summary_en,
            summary_ar=payload.summary_ar,
            credibility_score=payload.credibility_score
        )
        s.merge(b)
        s.commit()
        return {"status": "ok", "id": b.id}

class LegalIn(BaseModel):
    id: str
    title: str
    instrument_type: str
    country_id: str
    source_id: str
    number: str | None = None
    status: str | None = None
    adoption_date: str | None = None
    effective_date: str | None = None
    jurisdiction_id: str | None = None
    segments: list[str] = []
    related_projects: list[str] = []
    topics: list[str] = []
    original_lang: str | None = None
    summary_fr: str | None = None
    summary_en: str | None = None
    summary_ar: str | None = None
    credibility_score: float | None = None

@app.post("/legal", dependencies=[Depends(require_api_key)])
def create_legal(payload: LegalIn):
    with Session(engine) as s:
        li = LegalInstrument(
            id=payload.id,
            title=payload.title,
            instrument_type=payload.instrument_type,
            number=payload.number,
            status=payload.status,
            adoption_date=payload.adoption_date,
            effective_date=payload.effective_date,
            country_id=payload.country_id,
            jurisdiction_id=payload.jurisdiction_id,
            segments=payload.segments,
            related_projects=payload.related_projects,
            topics=payload.topics,
            source_id=payload.source_id,
            original_lang=payload.original_lang,
            summary_fr=payload.summary_fr,
            summary_en=payload.summary_en,
            summary_ar=payload.summary_ar,
            credibility_score=payload.credibility_score,
        )
        s.merge(li)
        s.commit()
        return {"status": "ok", "id": li.id}
