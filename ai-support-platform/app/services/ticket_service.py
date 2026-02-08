from datetime import datetime
from app.core.database import get_database
from app.models.ticket import Ticket

class TicketService:

    @staticmethod
    async def create_ticket(ticket: Ticket) -> Ticket:
        db = get_database()

        ticket.created_at = datetime.utcnow()
        ticket.updated_at = datetime.utcnow()

        
        data = ticket.dict(
            by_alias=True,
            exclude={"_id"},
            exclude_none=True
        )

        result = await db.tickets.insert_one(data)

        ticket.id = str(result.inserted_id)
        return ticket

    @staticmethod
    async def get_ticket(ticket_id: str) -> Ticket | None:
        db = get_database()
        data = await db.tickets.find_one({"_id": ticket_id})
        if not data:
            return None
        data["_id"] = str(data["_id"])
        return Ticket(**data)

    @staticmethod
    async def update_status(ticket_id: str, status: str, reason: str | None = None):
        db = get_database()
        update = {
            "status": status,
            "updated_at": datetime.utcnow()
        }
        if status in ["closed", "provisionally_resolved"]:
            update["resolved_at"] = datetime.utcnow()
            update["closed_reason"] = reason

        await db.tickets.update_one(
            {"_id": ticket_id},
            {"$set": update}
        )
