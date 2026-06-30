import random
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, field_validator

app = FastAPI()

class StudentRegister(BaseModel):
    full_name: str = Field(..., min_length=3)

    email: EmailStr

    age: int = Field(..., ge=15, le=60)

    phone: str = Field(..., min_length=10, max_length=11)
    
    course: str
    
    note: str | None = Field(default=None, max_length=200)

    @field_validator('phone')
    @classmethod
    def validate_phone_digits(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Số điện thoại chỉ được chứa các chữ số")
        return value


@app.post("/students/register")
def register_student(student: StudentRegister):

    normalized_name = student.full_name.title()

    student_id = f"HV-{random.randint(1000, 9999)}"

    student_data = student.model_dump()
    student_data["full_name"] = normalized_name 
    student_data["student_id"] = student_id     

    return {
        "message": "Đăng ký học viên thành công",
        "data": student_data
    }


"""
PHẦN 5: DANH SÁCH CÁC API THÀNH CÔNG VÀ THẤT BẠI

1. API Thành công (Dữ liệu hợp lệ)
- Request: POST /students/register
- Body mẫu gửi lên:
  {
    "full_name": "nguyen van an",
    "email": "anan@example.com",
    "age": 20,
    "phone": "0987654321",
    "course": "python",
    "note": "Muon hoc lop buoi toi"
  }
- Response mong muốn trả về:
  {
    "message": "Đăng ký học viên thành công",
    "data": {
      "student_id": "HV-4829",
      "full_name": "Nguyen Van An",
      "email": "anan@example.com",
      "age": 20,
      "phone": "0987654321",
      "course": "python",
      "note": "Muon hoc lop buoi toi"
    }
  }

2. API Thất bại (Dữ liệu không hợp lệ)
Khi client gửi dữ liệu sai, hệ thống tự động trả về mã lỗi 422 (Unprocessable Entity) kèm chi tiết lỗi cụ thể mà không làm sập server:

- STT 1: Thiếu email
  + Mô tả: Bỏ hoàn toàn trường "email" ra khỏi JSON gửi lên
  + Kết quả: Báo lỗi validate thiếu trường bắt buộc (Field required)

- STT 2: age nhỏ hơn 15
  + Mô tả: Gửi kèm "age": 14 trong body
  + Kết quả: Báo lỗi validate giá trị phải lớn hơn hoặc bằng 15 (Input should be greater than or equal to 15)

- STT 3: age lớn hơn 60
  + Mô tả: Gửi kèm "age": 65 trong body
  + Kết quả: Báo lỗi validate giá trị phải nhỏ hơn hoặc bằng 60 (Input should be less than or equal to 60)

- STT 4: phone chứa chữ cái
  + Mô tả: Gửi kèm "phone": "0987654abc" trong body
  + Kết quả: Báo lỗi validate tự định nghĩa (Value error, Số điện thoại chỉ được chứa các chữ số)

- STT 5: phone ngắn hơn 10 số
  + Mô tả: Gửi kèm "phone": "0987" trong body
  + Kết quả: Báo lỗi validate chuỗi quá ngắn (String should have at least 10 characters)

- STT 6: note dài hơn 200 ký tự
  + Mô tả: Gửi kèm chuỗi ghi chú dài vượt quá 200 chữ
  + Kết quả: Báo lỗi validate chuỗi dài vượt mức cho phép (String should have at most 200 characters)

"""