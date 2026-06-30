"""PHÂN TÍCH LỖI
Endpoint hiện tại có Path Parameter không? Là gì?
Có. Path Parameter là {status}
Khi gọi /orders/status/pending, biến status nhận giá trị gì?
Biến status nhận giá trị là chuỗi "pending"
Vì sao API trả về sai dữ liệu?
Vì code viết xong thì "để trưng" chứ không dùng
FastAPI nhận được chữ "pending" rồi nhưng trong hàm lại lười không lọc, cứ thế return thẳng luôn cả danh sách orders ban đầu
Dòng code làm API bỏ qua giá trị status:
return orders
"""

from fastapi import FastAPI

app = FastAPI()

orders = [
    {"id": 1, "customer_name": "Nguyễn Văn An", "total": 250000, "status": "pending"},
    {"id": 2, "customer_name": "Trần Thị Bình", "total": 500000, "status": "paid"},
    {"id": 3, "customer_name": "Lê Văn Cường", "total": 150000, "status": "cancelled"},
    {"id": 4, "customer_name": "Phạm Thị Dung", "total": 320000, "status": "pending"}
]

VALID_STATUSES = ["pending", "paid", "cancelled"]

@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    if status not in VALID_STATUSES:
        return {"message": "Trạng thái đơn hàng không hợp lệ"}
        
    filtered_orders = []
    for order in orders:
        if order["status"] == status:
            filtered_orders.append(order)
            
    return filtered_orders