# import dependencies
from __future__ import annotations
from sqlmodel import SQLModel, Relationship, Field, CheckConstraint, func
from typing import Optional, List
from datetime import date, datetime, time
from enum import Enum


# create passenger model
class Passenger(SQLModel, table=True):
    passenger_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(..., max_length=25)
    last_name: str = Field(..., max_length=25)
    email: str = Field(..., max_length=75, unique=True)
    birth_date: date = Field(...)
    phone_number: str = Field(..., max_length=18)
    
    flights: List[Flight] = Relationship(back_populates="passengers", link_model="Ticket")
    

# validate flight class
class FlightClass(str, Enum):
    first = "first"
    bussiness = "bussiness"
    economy = "economy"
    
    
class Flight(SQLModel, table=True):
    flight_id: Optional[int] = Field(default=None, primary_key=True)
    flight_number: str = Field(..., max_length=25)
    flight_class: FlightClass = Field(...)
    departure_time: datetime = Field(...,)
    arrival_time: datetime = Field(...)
    distance_in_miles: int = Field(...)
    fligth_duration: time = Field(...)
    destination: str = Field(..., max_length=25)
    __table_arg__ = (CheckConstraint("flight_class IN('first', 'bussiness', 'economy')"))
    
    passengers: List[Passenger] = Relationship(back_populates="flights", link_model="Ticket")

    
# create a link model
class Ticket(SQLModel, table=True):
    ticket_id: Optional[int] = Field(default=None, primary_key=True)
    passenger_id: int = Field(foreign_key="passenger.passenger_id")
    flight_id: int = Field(foreign_key="flight.flight_id")
    