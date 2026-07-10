from sqlalchemy.orm import Session
from app.models.product import ProductModel
from app.schemas.product import ProductCreate

class ProductService:
    @staticmethod
    def get_all(db: Session):
        return db.query(ProductModel).all()

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        return db.query(ProductModel).filter(ProductModel.id == product_id).first()

    @staticmethod
    def create(db: Session, product_data: ProductCreate):
        db_product = ProductModel(name=product_data.name, price=product_data.price)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def update(db: Session, product_id: int, product_data: ProductCreate):
        db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not db_product:
            return None
        
        db_product.name = product_data.name
        db_product.price = product_data.price
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def delete(db: Session, product_id: int):
        db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not db_product:
            return False
        
        db.delete(db_product)
        db.commit()
        return True