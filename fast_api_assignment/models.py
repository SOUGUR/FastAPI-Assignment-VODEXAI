from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional

class Item(BaseModel):
    _id: int  
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: date
    insert_date: date = Field(default_factory=date.today, exclude=True)

class UpdateItem(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    item_name: Optional[str] = None
    quantity: Optional[int] = None
    expiry_date: Optional[date] = None

class ClockIn(BaseModel):
    id: Optional[int]  
    email: str
    location: str
    insert_date: datetime = Field(default_factory=datetime.now, exclude=True)

class UpdateClockIn(BaseModel):
    email: Optional[EmailStr] = None
    location: Optional[str] = None