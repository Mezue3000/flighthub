# import dependencies
from __future__ import annotations
from sqlmodel import SQLModel, Relationship, Field, CheckConstraint, func
from typing import Optional, List
from datetime import date, datetime, timezone


# create passenger model
class Passenger(SQLModel, table=True):
    passenger_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(..., max_length=25)
    last_name: str = Field(..., max_length=25)
    email: str = Field(..., max_length=75, unique=True)
    birth_date: date = Field(...)
    phone_number: str = Field(..., max_length=18)
    