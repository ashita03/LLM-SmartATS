from sqlalchemy import create_engine, Column, Integer, String, DateTime, LargeBinary, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Create the database engine
engine = create_engine('sqlite:///job_applications.db', echo=True)
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

class Resume(Base):
    __tablename__ = 'resumes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_name = Column(String, nullable=False)
    content = Column(LargeBinary, nullable=False)  # Store PDF as binary
    upload_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)  # Flag for current active resume
    
    # Relationships
    user = relationship("User", back_populates="resumes")

class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
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
        db.close()
