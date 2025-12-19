
from sqlalchemy import Column, String, Float, DateTime
from app.db.database import Base

class FlightTracer(Base):
    __tablename__ = "flight_tracer"

    flight_number = Column(String(20), primary_key=True)
    airline = Column(String(50))
    origin = Column(String(50))
    destination = Column(String(50))
    departure = Column(DateTime)
    arrival = Column(DateTime)
    ticket_price = Column(Float)
