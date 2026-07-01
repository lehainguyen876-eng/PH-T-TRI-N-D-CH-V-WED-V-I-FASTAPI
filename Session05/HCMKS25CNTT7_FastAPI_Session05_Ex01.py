from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    for p in products:
        if p["code"] == product.code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sản phẩm với mã '{product.code}' đã tồn tại trong hệ thống."
            )
            
    new_product = {
        "id": len(products) + 1,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }
    
    products.append(new_product)
    return {
        "message": "Create product successfully",
        "data": new_product
    }

"""
BẢNG PHÂN TÍCH TEST CASE CHỨNG MINH API CŨ BỊ SAI LOGIC:

STT | Dữ liệu gửi lên (Body)                                              | Kết quả hiện tại (Cũ)           | Kết quả đúng mong muốn             | Lỗi phát hiện
----+---------------------------------------------------------------------+---------------------------------+------------------------------------+-------------------------------------------
1   | {"code": "SP001", "name": "Laptop ASUS", "price": 180000, "stock": 5}| Vẫn tạo được sản phẩm mới (HTTP 200)| Báo lỗi mã sản phẩm đã tồn tại (HTTP 400)| Không kiểm tra trùng mã sản phẩm (SP001)
2   | {"code": "SP002", "name": "Phím Akko", "price": 120000, "stock": 20} | Vẫn tạo được sản phẩm mới (HTTP 200)| Báo lỗi mã sản phẩm đã tồn tại (HTTP 400)| Không duyệt danh sách để validate mã trùng
"""