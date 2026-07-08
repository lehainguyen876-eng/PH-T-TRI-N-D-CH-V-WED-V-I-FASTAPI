from database import Base
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel, Field, field_validator

class ParkingSlotModel(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slot_code = Column(String(50), unique=True, nullable=False)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)

class slotreqdto(BaseModel):
    slot_code: str = Field(..., min_length=1)
    zone_name: str = Field(..., min_length=3)
    max_weight: int = Field(..., gt=0)

    @field_validator("slot_code", "zone_name")
    @classmethod
    def check_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Khong duoc de trong chuoi")
        return v