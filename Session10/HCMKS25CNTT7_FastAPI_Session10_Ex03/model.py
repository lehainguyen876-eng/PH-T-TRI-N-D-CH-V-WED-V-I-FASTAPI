from database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

class InventoryModel(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    warehouse_code = Column(String(50), unique=True, nullable=False)
    location = Column(String(100), nullable=False)

class InventoryCreateDTO(BaseModel):
    warehouse_code: str
    location: str