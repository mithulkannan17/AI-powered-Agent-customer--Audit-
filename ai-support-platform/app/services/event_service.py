from app.core.database import get_database
from app.models.event import Event

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
