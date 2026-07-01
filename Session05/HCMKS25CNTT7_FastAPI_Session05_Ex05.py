from fastapi import FastAPI, HTTPException, status

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "is_active": True},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "is_active": True},
    {"id": 3, "code": "SP003", "name": "Monitor", "price": 2500000, "is_active": False}
]

@app.delete("/products/{product_id}")
def deactivate_product(product_id: int):

    target_product = next((p for p in products if p["id"] == product_id), None)
    
    if not target_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Product not found"
        )
        
    if not target_product["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Product already inactive"
        )
    target_product["is_active"] = False
    return {
        "message": "Product has been discontinued successfully",
        "data": target_product
    }

"""
LUỒNG XỬ LÝ DỮ LIỆU KHI CLIENT GỬI REQUEST (DELETE /products/{product_id}):

1. Tiếp nhận request: 
   Client gửi request tới endpoint kèm theo `product_id` trên đường dẫn (Path Parameter).

2. Kiểm tra sự tồn tại (Tầng 1):
   - Hệ thống thực hiện quét danh sách `products` để tìm sản phẩm có ID trùng khớp.
   - Nếu KHÔNG tìm thấy sản phẩm -> Hệ thống dừng xử lý, lập tức phản hồi mã lỗi HTTP 404 (Product not found).

3. Kiểm tra trạng thái kinh doanh (Tầng 2):
   - Nếu TÌM thấy sản phẩm, hệ thống đọc tiếp giá trị của trường `is_active`.
   - Nếu `is_active == False` (Sản phẩm đã dừng bán trước đó) -> Hệ thống dừng xử lý, lập tức phản hồi mã lỗi HTTP 400 (Product already inactive).

4. Thực thi cập nhật trạng thái (Xử lý chính):
   - Nếu vượt qua 2 tầng kiểm tra trên (Sản phẩm có tồn tại và đang `is_active == True`).
   - Hệ thống tiến hành ghi đè thuộc tính `is_active = False` trực tiếp trên object đó trong list. Hành động này giúp giữ nguyên lịch sử, không làm mất mát data.

5. Trả về kết quả:
   - Hệ thống đóng gói dữ liệu gồm thông báo thành công và object sản phẩm vừa sửa trạng thái, phản hồi về Client với mã HTTP 200 OK.
"""