from fastapi import APIRouter, HTTPException
from typing import List
from app.models.ticket import Ticket
from app.services.ticket_service import TicketService
from app.core.database import get_database

router = APIRouter()

@router.post("/", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    return await TicketService.create_ticket(ticket)

@router.get("/", response_model=List[Ticket])
async def list_tickets():
    db = get_database()
    tickets = []
    async for t in db.tickets.find():
        t["_id"] = str(t["_id"])
        tickets.append(t)
    return tickets

@router.patch("/{ticket_id}/status")
async def update_ticket_status(ticket_id: str, status: str, reason: str | None = None):
    await TicketService.update_status(ticket_id, status, reason)
    return {"message": "Ticket status updated"}
