from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Khởi tạo lớp Base để các Class Model kế thừa
Base = declarative_base()

# ==========================================
# 5. THỰC THỂ TRUNG GIAN: BẢNG PHÂN PHỐI (Association Table)
# ==========================================
# Tên bảng trên cơ sở dữ liệu: package_truck
# Được định nghĩa bằng đối tượng Table của SQLAlchemy (không tạo class model riêng)
package_truck = Table(
    "package_truck",
    Base.metadata,
    # Cả hai cột này cùng hợp thành Khóa chính phức hợp (primary_key=True)
    Column("package_id", Integer, ForeignKey("packages.id"), primary_key=True),
    Column("truck_id", Integer, ForeignKey("trucks.id"), primary_key=True),
)


# ==========================================
# 1. THỰC THỂ 1: WAREHOUSE (Nhà kho)
# ==========================================
class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True)  # Khóa chính
    warehouse_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)

    # Mối quan hệ 1-N: Một Nhà kho có thể chứa Nhiều Kiện hàng (packages)
    # Khớp nối thuộc tính hai chiều bằng back_populates với class Package
    packages = relationship("Package", back_populates="warehouse")


# ==========================================
# 2. THỰC THỂ 2: PACKAGE (Kiện hàng)
# ==========================================
class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True)  # Khóa chính
    package_code = Column(
        String(100), unique=True, nullable=False
    )  # Đảm bảo mã kiện hàng không trùng lặp
    weight = Column(Float, nullable=False)

    # Khóa ngoại của quan hệ 1-N nằm ở bảng phía "Nhiều" (trỏ tới bảng Nhà kho)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    # Mối quan hệ N-1: Kiện hàng thuộc về Một Nhà kho duy nhất
    warehouse = relationship("Warehouse", back_populates="packages")

    # Mối quan hệ 1-1: Sở hữu Một Vận đơn chi tiết duy nhất (waybill)
    # Quy tắc cấu hình 1-1: chứa tham số uselist=False để trả về đối tượng đơn lẻ thay vì một danh sách
    waybill = relationship("Waybill", back_populates="package", uselist=False)

    # Mối quan hệ Nhiều - Nhiều (N-N): Được vận chuyển thông qua Nhiều Chuyến xe tải (trucks)
    # Bắt buộc cấu hình tham số secondary trỏ về bảng trung gian package_truck đã khai báo
    trucks = relationship("Truck", secondary=package_truck, back_populates="packages")


# ==========================================
# 3. THỰC THỂ 3: WAYBILL (Vận đơn chi tiết)
# ==========================================
class Waybill(Base):
    __tablename__ = "waybills"

    id = Column(Integer, primary_key=True)  # Khóa chính
    tracking_number = Column(String(100), nullable=False)
    shipping_status = Column(String(50), nullable=False)

    # Khóa ngoại liên kết tới bảng Kiện hàng
    # Bắt buộc có ràng buộc duy nhất (unique=True) ở bảng phụ để đảm bảo tính độc bản của quan hệ 1-1
    package_id = Column(Integer, ForeignKey("packages.id"), unique=True, nullable=False)

    # Mối quan hệ 1-1 đối ứng với thực thể Kiện hàng (package)
    package = relationship("Package", back_populates="waybill")


# ==========================================
# 4. THỰC THỂ 4: TRUCK (Xe tải vận chuyển)
# ==========================================
class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True)  # Khóa chính
    license_plate = Column(String(50), nullable=False)

    # Mối quan hệ Nhiều - Nhiều (N-N): Một Xe tải có thể vận chuyển Nhiều Kiện hàng khác nhau
    # Cấu hình tham số secondary trỏ về bảng trung gian package_truck
    packages = relationship("Package", secondary=package_truck, back_populates="trucks")