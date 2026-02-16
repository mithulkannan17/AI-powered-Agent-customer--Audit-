from datetime import datetime
from app.core.database import get_database
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.signal_extractor import SignalExtractor
from app.services.event_service import EventService
from app.services.intervention_service import InterventionService

class ConversationService:

    @staticmethod
    async def start_conversation(conversation: Conversation) -> Conversation:
        db = get_database()
        conversation.started_at = datetime.utcnow()

        data = conversation.dict(
            by_alias=True,
            exclude={"_id"},
            exclude_none=True
        )

        result = await db.conversations.insert_one(data)

        conversation.id = str(result.inserted_id)
        return conversation


    @staticmethod
    async def end_conversation(conversation_id: str):
        db = get_database()
        await db.conversations.update_one(
            {"_id": conversation_id},
            {"$set": {
                "status": "ended",
                "ended_at": datetime.utcnow()
            }}
        )

    @staticmethod
    async def add_message(message: Message) -> Message:
        db = get_database()

        data = message.dict(
            by_alias=True,
            exclude={"_id"},
            exclude_none=True
        )

        result = await db.messages.insert_one(data)

        message.id = str(result.inserted_id)

        events = SignalExtractor.extract_events(message)
        for event in events:
            await EventService.log_event(event)

        await InterventionService.evaluate(message.ticket_id)
            
        return message
