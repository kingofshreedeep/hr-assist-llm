from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "postgresql://postgres:sans@db:5432/talentscout"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    user_details = Column(JSON, nullable=True)  # Store user info like name, experience, etc.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)  # user or assistant
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    name = Column(String)
    experience_years = Column(Float)  # Extracted numeric experience
    experience_raw = Column(String)   # Original text
    position = Column(String)
    tech_stack = Column(JSON)         # Parsed technologies
    skills_extracted = Column(JSON)   # AI-extracted skills
    competency_level = Column(String) # junior/mid/senior
    technical_answer = Column(Text)   # Their technical response
    ai_assessment = Column(JSON)      # AI analysis of their answers
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Base.metadata.create_all(bind=engine)  # Moved to api.py startup