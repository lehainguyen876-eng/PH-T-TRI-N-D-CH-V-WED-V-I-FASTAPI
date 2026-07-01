from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date

app = FastAPI()

rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING"
    }
]

class RoomCreate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)
    status: Literal["AVAILABLE", "IN_USE", "MAINTENANCE"]

class RoomUpdate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)
    status: Literal["AVAILABLE", "IN_USE", "MAINTENANCE"]

class BookingCreate(BaseModel):
    room_id: int
    class_name: str = Field(..., min_length=1)
    student_count: int = Field(..., gt=0)
    date: date
    slot: Literal["MORNING", "AFTERNOON", "EVENING"]

@app.post("/rooms", status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate):
    if any(r["code"].upper() == room.code.upper() for r in rooms):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room code already exists")
    
    new_room = {
        "id": max([r["id"] for r in rooms], default=0) + 1,
        "code": room.code,
        "name": room.name,
        "capacity": room.capacity,
        "status": room.status
    }
    rooms.append(new_room)
    return {"message": "Room created successfully", "data": new_room}

@app.get("/rooms")
def get_rooms(
    keyword: Optional[str] = Query(None),
    status: Optional[Literal["AVAILABLE", "IN_USE", "MAINTENANCE"]] = Query(None),
    min_capacity: Optional[int] = Query(None, ge=1)
):
    filtered_rooms = rooms.copy()
    
    if keyword:
        keyword_lower = keyword.lower()
        filtered_rooms = [
            r for r in filtered_rooms 
            if keyword_lower in r["name"].lower() or keyword_lower in r["code"].lower()
        ]
        
    if status:
        filtered_rooms = [r for r in filtered_rooms if r["status"] == status]
        
    if min_capacity is not None:
        filtered_rooms = [r for r in filtered_rooms if r["capacity"] >= min_capacity]
        
    return filtered_rooms

@app.get("/rooms/{room_id}")
def get_room_detail(room_id: int):
    target_room = next((r for r in rooms if r["id"] == room_id), None)
    if not target_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return target_room

@app.put("/rooms/{room_id}")
def update_room(room_id: int, payload: RoomUpdate):
    target_room = next((r for r in rooms if r["id"] == room_id), None)
    if not target_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        
    if any(r["code"].upper() == payload.code.upper() and r["id"] != room_id for r in rooms):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room code already exists")
        
    target_room["code"] = payload.code
    target_room["name"] = payload.name
    target_room["capacity"] = payload.capacity
    target_room["status"] = payload.status
    
    return {"message": "Room updated successfully", "data": target_room}

@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    target_room = next((r for r in rooms if r["id"] == room_id), None)
    if not target_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        
    rooms.remove(target_room)
    return {"message": f"Room with ID {room_id} deleted successfully"}

@app.post("/room-bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate):
    target_room = next((r for r in rooms if r["id"] == booking.room_id), None)
    if not target_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        
    if target_room["status"] != "AVAILABLE":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room is not available for booking")
        
    if booking.student_count > target_room["capacity"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student count exceeds room capacity")
        
    booking_date_str = str(booking.date)
    if any(b["room_id"] == booking.room_id and b["date"] == booking_date_str and b["slot"] == booking.slot for b in room_bookings):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room is already booked for this date and slot")
        
    new_booking = {
        "id": max([b["id"] for b in room_bookings], default=0) + 1,
        "room_id": booking.room_id,
        "class_name": booking.class_name,
        "student_count": booking.student_count,
        "date": booking_date_str,
        "slot": booking.slot
    }
    room_bookings.append(new_booking)
    return {"message": "Room booked successfully", "data": new_booking}

@app.get("/room-bookings")
def get_room_bookings():
    return room_bookings