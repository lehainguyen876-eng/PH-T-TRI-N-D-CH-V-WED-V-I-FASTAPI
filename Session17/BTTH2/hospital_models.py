from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Khởi tạo lớp cơ sở (Base Class) cho các mô hình ORM
Base = declarative_base()

# ==========================================
# THỰC THỂ TRUNG GIAN: BẢNG KÊ ĐƠN (Association Table)
# ==========================================
# Tên bảng trên cơ sở dữ liệu: patient_medication
# Định nghĩa bằng đối tượng Table của SQLAlchemy (không tạo class model riêng)
patient_medication = Table(
    "patient_medication",
    Base.metadata,
    # Cả hai cột này cùng hợp thành Khóa chính phức hợp (primary_key=True)
    Column("patient_id", Integer, ForeignKey("patients.id"), primary_key=True),
    Column("medication_id", Integer, ForeignKey("medications.id"), primary_key=True),
)


# ==========================================
# THỰC THỂ 1: DOCTOR (Bác sĩ)
# ==========================================
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)  # Khóa chính
    name = Column(String(255), nullable=False)
    specialty = Column(String(255), nullable=False)

    # Mối quan hệ 1-N: Một Bác sĩ thăm khám và quản lý Nhiều Bệnh nhân (patients)
    patients = relationship("Patient", back_populates="doctor")


# ==========================================
# THỰC THỂ 2: PATIENT (Bệnh nhân)
# ==========================================
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)  # Khóa chính
    patient_code = Column(
        String(100), unique=True, nullable=False
    )  # Đảm bảo không trùng lặp

    # Khóa ngoại trỏ tới bảng Bác sĩ (Quan hệ 1-N nằm ở bảng con / phía "Nhiều")
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    # Mối quan hệ N-1: Bệnh nhân thuộc sự quản lý của Một Bác sĩ duy nhất
    doctor = relationship("Doctor", back_populates="patients")

    # Mối quan hệ 1-1: Sở hữu Một Sổ bảo hiểm y tế chi tiết duy nhất (insurance)
    # Quy tắc cấu hình 1-1: chứa tham số uselist=False để trả về 1 đối tượng đơn lẻ thay vì một danh sách
    insurance = relationship("Insurance", back_populates="patient", uselist=False)

    # Mối quan hệ Nhiều - Nhiều (N-N): Được kê và sử dụng Nhiều Loại thuốc điều trị
    # Cấu hình tham số secondary trỏ về bảng trung gian patient_medication đã khai báo
    medications = relationship(
        "Medication", secondary=patient_medication, back_populates="patients"
    )


# ==========================================
# THỰC THỂ 3: INSURANCE (Sổ bảo hiểm y tế)
# ==========================================
class Insurance(Base):
    __tablename__ = "insurances"

    id = Column(Integer, primary_key=True)  # Khóa chính
    insurance_number = Column(String(100), nullable=False)
    expiry_date = Column(Date, nullable=False)  # Kiểu dữ liệu ngày tháng

    # Khóa ngoại liên kết tới bảng Bệnh nhân
    # Bắt buộc có ràng buộc duy nhất (unique=True) để đảm bảo tính độc bản 1-1
    patient_id = Column(Integer, ForeignKey("patients.id"), unique=True, nullable=False)

    # Mối quan hệ 1-1 đối ứng với thực thể Bệnh nhân (patient)
    patient = relationship("Patient", back_populates="insurance")


# ==========================================
# THỰC THỂ 4: MEDICATION (Thuốc điều trị)
# ==========================================
class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True)  # Khóa chính
    name = Column(String(255), nullable=False)

    # Mối quan hệ Nhiều - Nhiều (N-N): Một Loại thuốc có thể được kê cho Nhiều Bệnh nhân
    patients = relationship(
        "Patient", secondary=patient_medication, back_populates="medications"
    )