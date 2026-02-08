from app.models.message import Message
from app.models.event import Event

ESCALATION_KEYWORDS = {
    "human", "agent", "manager", "support",
    "stop", "escalate", "refund now"
}

NEGATION_WORDS = {"no", "not", "wrong", "incorrect", "instead"}

class SignalExtractor:

    @staticmethod
    def extract_events(message: Message):
        events = []

        text = message.text.lower()

        # Explicit escalation request
        if any(word in text for word in ESCALATION_KEYWORDS):
            events.append(Event(
                ticket_id=message.ticket_id,
                conversation_id=message.conversation_id,
                message_id=message.id,
                event_type="EXPLICIT_ESCALATION",
                severity="critical",
                metadata={"text": message.text}
            ))

        #  Contextual correction signal 
        if message.sender_type == "customer":
            if any(word in text.split() for word in NEGATION_WORDS):
                events.append(Event(
                    ticket_id=message.ticket_id,
                    conversation_id=message.conversation_id,
                    message_id=message.id,
                    event_type="CONTEXTUAL_CORRECTION",
                    severity="warning",
                    metadata={"text": message.text}
                ))

        return events
