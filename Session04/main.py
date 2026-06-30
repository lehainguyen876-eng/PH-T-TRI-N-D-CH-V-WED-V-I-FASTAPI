""" Phần 1: Phân tích & Đề xuất đa giải pháp
Phân tích yêu cầu Input / Output:
nput: Dữ liệu học viên gửi lên dạng JSON gồm: full_name, email, age, course, phone
Output thành công: Trả về thông tin học viên vừa tạo kèm thông báo thành công
Output thất bại: Trả về nội dung lỗi cụ thể (detail) kèm mã lỗi phù hợp (ví dụ: Thiếu trường, Sai định dạng email, Trùng email)
Đề xuất 2 giải pháp:
Giải pháp 1 (Thủ công - Manual Validation): Nhận dữ liệu dưới dạng một dict thông thường hoặc qua Body(), sau đó dùng các câu lệnh điều kiện if-else thuần Python để kiểm tra từng quy tắc (độ dài tên, kiểm tra dấu @ trong email, kiểm tra xem có truyền đủ trường không)
Giải pháp 2 (Tự động - Pydantic Model): Khai báo một class kế thừa từ BaseModel của Pydantic. Định nghĩa kiểu dữ liệu, dùng Field để bắt độ dài ký tự và dùng kiểu dữ liệu EmailStr để tự động check định dạng email

PHẦN 2: SO SÁNH & LỰA CHỌN

1. Bảng so sánh các giải pháp

| Tiêu chí | Giải pháp 1: Kiểm tra thủ công (if-else) | Giải pháp 2: Dùng Pydantic Model |
| :--- | :--- | :--- |
| Độ dễ hiểu | Rất dễ hiểu vì chỉ dùng logic Python căn bản. | Cần học thêm cú pháp khai báo Class của Pydantic. |
| Số lượng code cần viết | Viết rất nhiều, dài dòng vì phải check if-else cho từng trường. | Rất ngắn gọn, khai báo kiểu dữ liệu xong là xong. |
| Khả năng kiểm soát lỗi | Dễ sót bẫy dữ liệu (như client gửi thiếu trường hoặc sai kiểu dữ liệu). | Cực tốt. FastAPI và Pydantic tự động chặn đứng lỗi dữ liệu ngay từ vòng gửi xe. |
| Độ rõ ràng của cấu trúc | Kém. Không có một bộ khung mẫu nào định hình cho dữ liệu. | Rất rõ ràng. Nhìn vào Class là biết ngay cấu trúc JSON cần gửi lên. |

2. Chốt lựa chọn giải pháp phù hợp

Lựa chọn: Giải pháp 1 (Kiểm tra thủ công với if-else).

Lý do lựa chọn:
- Giải pháp này sử dụng các câu lệnh rẽ nhánh if-else và các hàm xử lý chuỗi căn bản của Python nên cực kỳ trực quan, dễ hiểu và dễ kiểm soát luồng chạy đối với sinh viên năm 1.
- Việc tự viết logic kiểm tra giúp hiểu sâu hơn về bản chất các bẫy dữ liệu (như cách kiểm tra chuỗi rỗng, bắt lỗi thiếu key trong dict hoặc duyệt mảng để tìm trùng email) trước khi phụ thuộc vào các thư viện tự động hóa nâng cao như Pydantic.
"""

from fastapi import FastAPI, Body

app = FastAPI()

# Giả lập database học viên
students_db = [
    {
        "full_name": "Nguyen Van An",
        "email": "existing@gmail.com",
        "age": 21,
        "course": "python",
        "phone": "0123456789"
    }
]

@app.post("/students")
def create_student(data: dict = Body(...)):
    if "full_name" not in data or "email" not in data:
        return {"detail": "Thiếu trường dữ liệu bắt buộc (full_name hoặc email)"}
        
    full_name = data.get("full_name")
    email = data.get("email")
    

    if not full_name or len(full_name.strip()) < 3:
        return {"detail": "Họ tên không được để trống và phải dài từ 3 ký tự trở lên"}
        
    if "@" not in email or "." not in email:
        return {"detail": "Email sai định dạng (thiếu @ hoặc dấu chấm)"}
        

    for student in students_db:
        if student["email"] == email:
            return {"detail": "Email đã tồn tại trong hệ thống"}
            

    students_db.append(data)
    return {
        "message": "Đăng ký học viên thành công",
        "data": data
    }