# Prefer backend-local implementation
from .models_impl import SessionLocal, ChatSession, Message, CandidateProfile, engine, Base

__all__ = ['SessionLocal', 'ChatSession', 'Message', 'CandidateProfile', 'engine', 'Base']

