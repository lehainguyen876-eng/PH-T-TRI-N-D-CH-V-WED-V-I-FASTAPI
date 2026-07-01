from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]

class ProductUpdate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

@app.put("/products/{product_id}")
def update_product(product_id: int, payload: ProductUpdate):
    target_product = next((p for p in products if p["id"] == product_id), None)
    if not target_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
    if any(p["code"] == payload.code and p["id"] != product_id for p in products):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product code already exists")
        
    target_product.update(payload.model_dump())
    return target_product

"""
PHẦN 1: PHÂN TÍCH INPUT/OUTPUT & ĐỀ XUẤT
1. Input/Output:
   - Input: Path Parameter `product_id` (int) và JSON Body (code, name, price, stock).
   - Output: Thành công trả về HTTP 200 + sản phẩm mới. Thất bại trả về HTTP 400/404/422 + detail lỗi.
2. Đề xuất giải pháp:
   - GP1 (Duyệt List): Dùng vòng lặp duyệt mảng gốc tìm ID và check trùng mã.
   - GP2 (Dùng Dict): Chuyển mảng sang cấu trúc Key-Value {id: product} để tìm kiếm trực tiếp.

PHẦN 2: SO SÁNH & LỰA CHỌN
- Tốc độ tìm kiếm: GP1: O(n) [Chậm] | GP2: O(1) [Nhanh].
- Bộ nhớ:          GP1: Tối ưu     | GP2: Tốn thêm bộ nhớ.
- Dễ hiểu/Bảo trì: GP1: Dễ/Thấp    | GP2: Trung bình/Cao.
- Bối cảnh:        GP1: Data nhỏ   | GP2: Data lớn, thực tế.

* Kết luận chọn: Áp dụng GP1 (Duyệt List) kết hợp hàm built-in tối ưu của Python để vừa đạt hiệu năng tốt 
  vừa giữ nguyên cấu trúc mảng dữ liệu ban đầu của đề bài.
"""