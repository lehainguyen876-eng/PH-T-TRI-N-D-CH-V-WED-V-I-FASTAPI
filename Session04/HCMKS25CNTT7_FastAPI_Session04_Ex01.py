"""PHÂN TÍCH LỖI
Tại sao bị lỗi 404 Not Found?
Vì FastAPI đang hiểu /products/product_id là một cái tên cố định bằng chữ, chứ không biết product_id là một biến số
Khi gõ /products/1, máy tìm không thấy trang nào tên là "1" nên báo lỗi 404
Dòng code viết sai:@app.get("/products/product_id")
Tại sao sai?
Thiếu cặp dấu ngoặc nhọn {}
Trong FastAPI, muốn máy hiểu là "biến" (Path Parameter) thì bắt buộc phải bọc nó lại thành {product_id}
Sửa lại cho đúng:@app.get("/products/{product_id}")
    """

from fastapi import FastAPI, HTTPException, status

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop Dell", "price": 15000000},
    {"id": 2, "name": "Chuột Logitech", "price": 350000},
    {"id": 3, "name": "Bàn phím cơ", "price": 1200000}
]


@app.get("/products/{product_id}")
def get_product_detail(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Không tìm thấy sản phẩm"
    )