from fastapi import FastAPI, HTTPException, status, Request
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime, timezone

app = FastAPI(
    title="Cinema Ticket Booking API"
)

tickets_db = [
    {"id": 1, "movie_name": "Doctor Strange 3", "room_code": "IMAX-01", "quantity": 2, "status": "confirmed", "created_at": "2026-07-01T19:00:00Z"},
    {"id": 2, "movie_name": "Avatar 3", "room_code": "PREMIUM-02", "quantity": 1, "status": "confirmed", "created_at": "2026-07-01T20:15:00Z"}
]

class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any]
    error: Optional[Any]
    timestamp: str
    path: str


class TicketRequest(BaseModel):
    movie_name: str = Field(..., min_length=1)
    room_code: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=10)


def success_response(statusCode: int, message: str, data: Any, request: Request):
    return APIResponse(
        statusCode=statusCode,
        message=message,
        data=data,
        error=None,
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=request.url.path
    )


@app.get("/tickets")
def get_tickets(request: Request):
    return success_response(
        200,
        "Lấy danh sách vé thành công!",
        tickets_db,
        request
    )


@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketRequest, request: Request):

    for t in tickets_db:
        if t["movie_name"] == ticket.movie_name and t["room_code"] == ticket.room_code:
            raise HTTPException(status_code=400)

    new_ticket = {
        "id": len(tickets_db) + 1,
        "movie_name": ticket.movie_name,
        "room_code": ticket.room_code,
        "quantity": ticket.quantity,
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    tickets_db.append(new_ticket)

    return success_response(
        201,
        "Đặt vé thành công!",
        new_ticket,
        request
    )


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, request: Request):

    ticket = next((t for t in tickets_db if t["id"] == ticket_id), None)

    if ticket is None:
        raise HTTPException(status_code=404)

    tickets_db.remove(ticket)

    return success_response(
        200,
        "Hủy vé thành công!",
        None,
        request
    )