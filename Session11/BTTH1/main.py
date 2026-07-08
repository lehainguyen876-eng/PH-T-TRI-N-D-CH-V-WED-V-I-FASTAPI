from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db, Base, engine
from model import ParkingSlotModel, slotreqdto

app = FastAPI()

Base.metadata.create_all(bind=engine)

def build_response(status_code, message, data, error, path):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "error": error,
            "data": data,
            "path": path,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )

@app.post("/parking-slots")
def add_slot(slot: slotreqdto, request: Request, db: Session = Depends(get_db)):
    try:
        existing = db.query(ParkingSlotModel).filter(ParkingSlotModel.slot_code == slot.slot_code).first()
        if existing:
            return build_response(400, "Ma vi tri do xe da ton tai", None, "Bad Request", request.url.path)

        new_slot = ParkingSlotModel(
            slot_code=slot.slot_code,
            zone_name=slot.zone_name,
            max_weight=slot.max_weight
        )
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        
        res_data = {
            "id": new_slot.id,
            "slot_code": new_slot.slot_code,
            "zone_name": new_slot.zone_name,
            "max_weight": new_slot.max_weight,
            "is_available": new_slot.is_available
        }
        return build_response(201, "Them vi tri do xe thanh cong", res_data, None, request.url.path)
    except Exception as e:
        db.rollback()
        return build_response(500, "Loi he thong", None, str(e), request.url.path)

@app.get("/parking-slots")
def list_slots(request: Request, db: Session = Depends(get_db)):
    try:
        slots = db.query(ParkingSlotModel).all()
        res_list = []
        for s in slots:
            res_list.append({
                "id": s.id,
                "slot_code": s.slot_code,
                "zone_name": s.zone_name,
                "max_weight": s.max_weight,
                "is_available": s.is_available
            })
        return build_response(200, "Lay danh sach vi tri do xe thanh cong", res_list, None, request.url.path)
    except Exception as e:
        return build_response(500, "Loi he thong", None, str(e), request.url.path)

@app.get("/parking-slots/{slot_id}")
def detail_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        s = db.query(ParkingSlotModel).filter(ParkingSlotModel.id == slot_id).first()
        if not s:
            return build_response(404, "Parking slot not found", None, "Not Found", request.url.path)
            
        res_data = {
            "id": s.id,
            "slot_code": s.slot_code,
            "zone_name": s.zone_name,
            "max_weight": s.max_weight,
            "is_available": s.is_available
        }
        return build_response(200, "Lay chi tiet vi tri do xe thanh cong", res_data, None, request.url.path)
    except Exception as e:
        return build_response(500, "Loi he thong", None, str(e), request.url.path)