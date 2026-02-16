from app.services.irr_predictor import IRRPredictor
from app.services.event_service import EventService

RISK_THRESHOLD = 0.75

class InterventionService:

    @staticmethod
    async def evaluate(ticket_id: str):
        prediction = await IRRPredictor.predict(ticket_id)

        # If ticket already labeled, ignore
        if "predicted_irr" not in prediction:
            return

        risk_score = 1 - prediction["confidence"] if prediction["predicted_irr"] == 1 else prediction["confidence"]

        # High risk of failure
        if risk_score >= RISK_THRESHOLD:
            event = {
                "ticket_id": ticket_id,
                "event_type": "HIGH_FAILURE_RISK",
                "severity": "warning"
            }

            await EventService.log_event(event)

            return {
                "intervention": True,
                "risk_score": round(risk_score, 3)
            }

        return {"intervention": False}
