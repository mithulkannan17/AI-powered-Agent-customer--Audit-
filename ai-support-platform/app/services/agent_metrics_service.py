from app.core.database import get_database

class AgentMetricsService:

    @staticmethod
    async def compute_leaderboard():
        db = get_database()

        pipeline = [
            {
                "$match": {
                    "agent_id": {"$ne": None},
                    "irr_label": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": "$agent_id",
                    "total_tickets": {"$sum": 1},
                    "resolved": {
                        "$sum": {
                            "$cond": [{"$eq": ["$irr_label", 1]}, 1, 0]
                        }
                    },
                    "unresolved": {
                        "$sum": {
                            "$cond": [{"$eq": ["$irr_label", 0]}, 1, 0]
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "irr_score": {
                        "$round": [
                            {"$divide": ["$resolved", "$total_tickets"]},
                            2
                        ]
                    }
                }
            },
            {
                "$sort": {"irr_score": -1}
            }
        ]

        leaderboard = await db.tickets.aggregate(pipeline).to_list(None)

        for agent in leaderboard:
            esc_count = await db.events.count_documents({
                "agent_id": agent["_id"],
                "event_type": "EXPLICIT_ESCALATION"
            })

            agent["escalations"] = esc_count
            agent["penalty_score"] = esc_count + agent["unresolved"]

        return leaderboard
