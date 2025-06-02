from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    LargeBinary,
    String
)
from database import engine, Base

class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True, nullable=False)
    pictures = Column(LargeBinary, nullable=False)  # store image bytes
    license_plate = Column(String,nullable=False)
    lane_id = Column(Integer, nullable=False)  # lane ID where the violation occurred

# Create tables
Base.metadata.create_all(bind=engine)