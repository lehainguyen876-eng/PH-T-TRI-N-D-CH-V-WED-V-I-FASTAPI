from sqlalchemy.orm import Session
from model import *

def create_product(db: Session, product: ProductCreateDTO):
    try:
        new_product = ProductModel(
            sku=product.sku,
            name=product.name,
            price=product.price
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {
            "status_code": 201,
            "message": "Tao san pham thanh cong"
        }
    except Exception as e:
        db.rollback()
        raise ValueError(f"Loi khi tao san pham: {str(e)}")