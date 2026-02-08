from app.models.event import Event
from app.services.ticket_service import TicketService

class EventDispatcher:

    @staticmethod
    async def handle_event(event: Event):
        
        if event.event_type == "EXPLICIT_ESCALATION":
            await TicketService.escalate_ticket(
                ticket_id=event.ticket_id,
                reason="User explicitly requested escalation"
            )
            return

        if event.event_type == "CONTEXTUAL_CORRECTION":
            await TicketService.add_risk_flag(
                ticket_id=event.ticket_id,
                flag="context_mismatch"
            )
