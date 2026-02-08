from app.core.database import get_database
from app.models.event import Event
from app.services.event_dispatcher import EventDispatcher

class EventService:

    @staticmethod
    async def log_event(event: Event):
        db = get_database()

        data = event.dict(
            by_alias=True,
            exclude={"_id"},
            exclude_none=True
        )

        await db.events.insert_one(data)

        await EventDispatcher.handle_event(event)
