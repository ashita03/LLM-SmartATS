# db_schema.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, LargeBinary, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Use an absolute path for the SQLite database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'job_applications.db')
engine = create_engine(f'sqlite:///{db_path}', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user")
    applications = relationship("Application", back_populates="user")

# In db_schema.py, modify the Resume model
class Resume(Base):
    __tablename__ = 'resumes'
    
    id = Column(Integer, primary_key=True)
    user_email = Column(String, ForeignKey('users.email'))  # Change Integer to String
    file_name = Column(String, nullable=False)
    content = Column(LargeBinary, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="resumes")

class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    user_email = Column(String, ForeignKey('users.email'))
    company_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    job_description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # Track application status
    
    # Store generated content
    cover_letter = Column(String)
    networking_email = Column(String)
    resume_review = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="applications")

# Create database tables
Base.metadata.create_all(engine)

# Create session factory
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.expunge_all()
        db.close()
