"""BÁO CÁO PHÂN TÍCH
Input của bài toán:
Danh sách cứng (hardcoded) gồm 4 sản phẩm product
2 tham số không bắt buộc từ URL (Query Parameters): keyword (chuỗi chữ) và max_price (số thực)
Output mong muốn:
Một danh sách các sản phẩm đã được lọc thỏa mãn điều kiện
Hoặc một thông báo lỗi nếu dữ liệu đầu vào không hợp lệ (max_price < 0)
Đề xuất giải pháp và các bước xử lý:
Bước 1: Kiểm tra điều kiện lỗi trước (Validation): Nếu có max_price và nó < 0, trả về thông báo lỗi ngay lập tức
Bước 2: Tạo một danh sách rỗng hoặc bản sao để chứa kết quả lọc. Ban đầu mặc định nó chứa tất cả sản phẩm
Bước 3: Lọc theo keyword (nếu có): Duyệt qua danh sách, chuyển cả tên sản phẩm và keyword về chữ thường (.lower()) để so sánh chứa chuỗi (in)
Bước 4: Lọc theo max_price (nếu có): Giữ lại các sản phẩm có price nhỏ hơn hoặc bằng max_price
Bước 5: Trả về danh sách kết quả cuối cùng
    """


from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]

@app.get("/products")
def get_products(keyword: str = None, max_price: float = None):
    if max_price is not None and max_price < 0:
        return {"detail": "max_price không được âm"}
        
    filtered_products = products
    
    if keyword is not None:
        filtered_products = [
            p for p in filtered_products 
            if keyword.lower() in p["name"].lower()
        ]
        
    if max_price is not None:
        filtered_products = [
            p for p in filtered_products 
            if p["price"] <= max_price
        ]
        
    return filtered_products