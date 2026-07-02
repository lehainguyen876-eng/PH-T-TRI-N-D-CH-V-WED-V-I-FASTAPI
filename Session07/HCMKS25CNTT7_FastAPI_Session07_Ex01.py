from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Manager Orders")

orders_db = [
    {
        "id": 1,
        "customer_name": "Nguyen Van A",
        "total_amount": 1500000.0,
        "profit_margin": 0.25,      
        "supplier_id": "SUP_DELL_01"
    },
    {
        "id": 2,
        "customer_name": "Tran Thi B",
        "total_amount": 350000.0,
        "profit_margin": 0.30,       
        "supplier_id": "SUP_LOGI_02"  
    }
]

class OrderResponseDTO(BaseModel):
    id: int
    customer_name: str
    total_amount: float

@app.get("/orders/{order_id}", response_model=OrderResponseDTO)
def get_order_detail(order_id: int):
    order_find = next((order for order in orders_db if order.get("id") == order_id), None)
    
    if order_find is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    
    return order_find


#  BÁO CÁO KẾT QUẢ TEST CASE 
# ===================================================================================================
# STT | Dữ liệu gửi lên | Kết quả hiện tại (Mã HTTP + Body)                 | Kết quả đúng mong muốn                           | Lỗi phát hiện
# -----------------------------------------------------------------------------------------------------------------------------------
# 1   | order_id = 999  | HTTP 404 Not Found                                | HTTP 404 Not Found                               | Đã sửa lỗi mã trạng thái "ảo" (Thay vì trả về 200 OK
#     |                 | {"detail": "Order not found"}                     | {"detail": "Order not found"}                     | kèm message, hệ thống đã báo lỗi 404 chuẩn RESTful).
# -----------------------------------------------------------------------------------------------------------------------------------
# 2   | order_id = 1    | HTTP 200 OK                                       | HTTP 200 OK                                       | Đã sửa lỗi lộ thông tin nhạy cảm (Sử dụng Response DTO
#     |                 | {"id": 1, "customer_name": "Nguyen Van A", ...}   | {"id": 1, "customer_name": "Nguyen Van A", ...}   | để tự động lọc, ẩn hoàn toàn 'profit_margin' và 'supplier_id').
