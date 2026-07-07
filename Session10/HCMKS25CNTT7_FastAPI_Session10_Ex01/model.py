from database import Base
from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

class ProductCreateDTO(BaseModel):
    sku: str
    name: str
    price: float