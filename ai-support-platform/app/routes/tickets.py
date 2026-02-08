from fastapi import APIRouter, HTTPException
from typing import List
from app.models.ticket import Ticket
from app.services.ticket_service import TicketService
from app.core.database import get_database
from app.services.outcome_service import OutcomeService
from app.services.irr_predictor import IRRPredictor


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

@router.post("/{ticket_id}/evaluate-out")
async def evaluate_outcome(ticket_id: str):
    await OutcomeService.evaluate_ticket_outcome(ticket_id)
    return {"message": "Outcome evaluated"}


@router.get("/{ticket_id}/predict-irr")
async def predict_irr(ticket_id: str):
    return await IRRPredictor.predict(ticket_id)