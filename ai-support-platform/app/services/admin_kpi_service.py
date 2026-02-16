from app.core.database import get_database

class AdminKPIService:

    @staticmethod
    async def get_kpis():
        db = get_database()

        total_tickets = await db.tickets.count_documents({})
        labeled = await db.tickets.count_documents({"irr_label": {"$ne": None}})
        resolved = await db.tickets.count_documents({"irr_label": 1})
        escalations = await db.events.count_documents({
            "event_type": "EXPLICIT_ESCALATION"
        })

        resolved_rate = round(resolved / labeled, 2) if labeled else 0

        return {
            "total_tickets": total_tickets,
            "labeled_tickets": labeled,
            "resolution_rate": resolved_rate,
            "escalations": escalations
        }
