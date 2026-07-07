from sqlalchemy.orm import Session
from model import *

def create_inventory(db: Session, inventory: InventoryCreateDTO):
    existing_inventory = db.query(InventoryModel).filter(
        InventoryModel.warehouse_code == inventory.warehouse_code
    ).first()

    if existing_inventory:
        raise ValueError("Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng")

    try:
        new_inventory = InventoryModel(
            warehouse_code=inventory.warehouse_code,
            location=inventory.location
        )
        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)

        return {
            "status_code": 201,
            "message": "Kho van da duoc khoi tao thanh cong"
        }
    except Exception as e:
        db.rollback()
        raise Exception(f"Loi he thong: {str(e)}")