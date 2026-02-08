from datetime import datetime, timedelta
from bson import ObjectId
from app.core.database import get_database

INACTIVITY_DAYS = 3

class OutcomeService:

    @staticmethod
    async def evaluate_ticket_outcome(ticket_id: str):
        db = get_database()
        oid = ObjectId(ticket_id)

        ticket = await db.ticket.find_one({"_id": oid})
        if not ticket:
            return
        
        if ticket.get("irr_label") is not None:
            return
        
        if ticket.get("status") == "open":
            await OutcomeService._mark_resolved(oid)

    
    @staticmethod
    async def _mark_resolved(oid: ObjectId):
        db = get_database()

        await db.tickets.update_one(
            {"_id": oid},
            {"$set": {
                "irr_label": 1,
                "irr_confidence": 0.7,
                "outcome_determined_at": datetime.utcnow()
            }}
        )

    @staticmethod
    async def _mark_unresolved(oid: ObjectId):
        db = get_database()
        await db.tickets.update_one(
            {"_id": oid},
            {"$set": {
                "irr_label": 0,
                "irr_confidence": 0.9,
                "outcome_determined_at": datetime.utcnow()
            }}
        )