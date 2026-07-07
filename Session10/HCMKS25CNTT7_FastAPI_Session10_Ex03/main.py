from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from model import *
from inventory_service import create_inventory

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/inventories", status_code=status.HTTP_201_CREATED)
def add_inventory(inventory: InventoryCreateDTO, db: Session = Depends(get_db)):
    try:
        result = create_inventory(db=db, inventory=inventory)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))