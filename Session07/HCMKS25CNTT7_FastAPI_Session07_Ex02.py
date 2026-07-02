from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI(title="Manager Orders - Fix Status")

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]


class StatusUpdate(BaseModel):
    status: OrderStatus 

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return next((o for o in orders_db if o["id"] == order_id), None)

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    
    order["status"] = data.status.value
    
    return {
        "status_code": 200,
        "message": "Cập nhật thành công",
        "data": order
    }


#  BÁO CÁO KẾT QUẢ TEST CASE
# ===================================================================================================
# STT | Dữ liệu/Endpoint gửi lên             | Kết quả sau khi sửa (Mã HTTP + Body)                 | Trạng thái lỗi ban đầu
# -----------------------------------------------------------------------------------------------------------------------------------
# 1   | PUT /orders/999/status                | HTTP 404 Not Found                                   | Đã sửa lỗi lọt luồng xử lý: Sử dụng `raise` thay 
#     | Body: {"status": "SHIPPING"}          | {"detail": "Order not found"}                        | vì `print()`, chặn đứng việc trả về mã 200 OK "ảo".
# -----------------------------------------------------------------------------------------------------------------------------------
# 2   | PUT /orders/1/status                  | HTTP 422 Unprocessable Entity                        | Đã loại bỏ Magic Number: Sử dụng `Enum`. Khi truyền sai
#     | Body: {"status": "TRONG_SANG"}        | {"detail": [{"msg": "Input should be 'PENDING'..."}]}| trạng thái, hệ thống tự động chặn từ vòng gửi xe với mã 422.