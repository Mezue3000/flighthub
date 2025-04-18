# import dependencies
from __future__ import annotations
from sqlmodel import SQLModel, Relationship, Field, CheckConstraint, func
from typing import Optional, List
from datetime import date, datetime, time, timezone
from enum import Enum
from decimal import Decimal


# create passenger model
class Passenger(SQLModel, table=True):
    passenger_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(..., max_length=25)
    last_name: str = Field(..., max_length=25)
    email: str = Field(..., max_length=75, unique=True)
    birth_date: date = Field(...)
    phone_number: str = Field(..., max_length=18)
    
    flights: List[Flight] = Relationship(back_populates="passengers", link_model="Ticket")
    

# validate flight class(api validation)
class FlightClass(str, Enum):
    first = "first"
    bussiness = "bussiness" 
    economy = "economy"
    
    
# create flight model    
class Flight(SQLModel, table=True):
    flight_id: Optional[int] = Field(default=None, primary_key=True)
    flight_number: str = Field(..., max_length=25)
    flight_class: FlightClass = Field(...)
    departure_time: datetime = Field(...)
    arrival_time: datetime = Field(...)
    distance_in_miles: int = Field(...)
    fligth_duration: time = Field(...)
    destination: str = Field(..., max_length=25)
    airline_id: int = Field(foreign_key="airline.airline_id")
    
    airline:Airline = Relationship(back_populates="flight")
    airports: List[Airport] = Relationship(back_populates="flights", link_model="Flight_Airport")
# database validation
    __table_arg__ = (CheckConstraint("flight_class IN('first', 'bussiness', 'economy')"))
    
    passengers: List[Passenger] = Relationship(back_populates="flights", link_model="Ticket")
    baggages:List[Baggage] = Relationship(back_populates="flight")

    
# create a link model
class Ticket(SQLModel, table=True):
    ticket_id: Optional[int] = Field(default=None, primary_key=True)
    passenger_id: int = Field(foreign_key="passenger.passenger_id")
    flight_id: int = Field(foreign_key="flight.flight_id")
    payment:Payment = Relationship(back_populates="ticket", sa_relationship_kwargs={"uselist": False})
    
    

# validate payment method(api validation)
class PaymentMethod(str, Enum):
    creditcard = "creditcard"
    debitcard = "debitcard"
    cash = "cash"


# create payment table
class Payment(SQLModel, table=True):
    ticket_id: int = Field(primary_key=True, foreign_key="ticket.ticket_id")
    amount: Decimal = Field(gt=0, sa_column_kwargs={"type": "Numeric(12, 2)"})
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    payment_method: PaymentMethod = Field(..., max_length=12)

# database validation
    __table_arg__ = (CheckConstraint("payment_method IN('creditcard', 'debitcard', 'cash')"))
    
    ticket:Ticket = Relationship(back_populates="payment") 
    

# create airline model
class Airline(SQLModel, table=True):
    airline_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=25)
    flights: List[Flight] = Relationship(back_populates="airline") 
    aircrafts: List[Aircraft] = Relationship(back_populates="airline")
    
    
# create aircraft table
class Aircraft(SQLModel, table=True):
    aircraft_id: Optional[int] = Field(default=None, primary_key=True)
    model: str = Field(..., max_length=25)
    capacity: int = Field(..., gt=0)
    airline_id: int = Field(foreign_key="airline.airline_id") 
    
    airline:Airline = Relationship(back_populates="aircraft")
    
    
# create airport model
class Airport(SQLModel, table=True):
    airport_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=25)
    code: str = Field(...)
    country: str = Field(..., max_length=25)
    state: str = Field(..., max_length=25)
    
    flights: List[Flight] = Relationship(back_populates="airports", link_model="AirportFlight")

# validate flight type(api validation)
class FlightType(str, Enum):
    departure = "departure"
    arrival = "arrival"


# add link model
class AirportFlight(SQLModel, table=True):
    flight_id: int =  Field(primary_key=True, foreign_key="flight.flight_id")
    airport_id: int = Field(primary_key=True, foreign_key="airport.airport_id")
    flight_type: FlightType = Field(..., max_length=12)

# database valdation    
    __table_arg__ = CheckConstraint("flight_type IN('arrival', 'departure')", name="valid_flight_type")


# validate baggage type(api validation)
class BaggageType(str, Enum):
    checked = "checked"
    hand = "hand"
    carried = "carried"
 
 
#  create baggage model   
class Baggage(SQLModel, table=True):
    baggage_id: Optional[int] = Field(default=None, primary_key=True)
    baggage_type: BaggageType = Field(..., max_length=10)
    weight_in_kg: int = Field(..., gt=0)
    flight_id: int = Field(foreign_key="flight.flight_id")
    
    flight: Flight = Relationship(back_populates="baggages")
    
    __table_arg__ = (CheckConstraint("baggage_type IN('chhecked', 'hand', 'carried')", name="valid_baggage_type"))