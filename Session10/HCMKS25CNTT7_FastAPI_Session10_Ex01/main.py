from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from model import *
from product_service import create_product

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreateDTO, db: Session = Depends(get_db)):
    try:
        result = create_product(db=db, product=product)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))