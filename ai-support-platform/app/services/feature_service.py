from bson import ObjectId
from app.core.database import get_database

class FeatureService:

    @staticmethod
    async def extract_features(ticket_id: str) -> dict:
        db = get_database()
        oid = ObjectId(ticket_id)

        messages = await db.messages.find(
            {"ticket_id": ticket_id}
        ).to_list(None)

        events = await db.events.find(
            {"ticket_id": ticket_id}
        ).to_list(None)

        features = {}

        # Message counts
        features["num_messages"] = len(messages)
        features["num_customer_messages"] = sum(
            1 for m in messages if m["sender_type"] == "customer"
        )
        features["num_agent_messages"] = sum(
            1 for m in messages if m["sender_type"] == "agent"
        )

        # Agent confidence
        agent_conf = [
            m.get("confidence") for m in messages
            if m["sender_type"] == "agent" and m.get("confidence") is not None
        ]
        features["avg_agent_confidence"] = (
            sum(agent_conf) / len(agent_conf)
            if agent_conf else 0.0
        )

        # Events
        features["has_escalation"] = any(
            e["event_type"] == "EXPLICIT_ESCALATION" for e in events
        )
        features["num_context_corrections"] = sum(
            1 for e in events if e["event_type"] == "CONTEXTUAL_CORRECTION"
        )

        return features
