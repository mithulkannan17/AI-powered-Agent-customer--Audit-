import os
import joblib
from bson import ObjectId
from app.core.database import get_database
from fastapi import HTTPException
from app.services.feature_service import FeatureService

MODEL_PATH = "irr_model.joblib"
_model = None


def get_model():
    global _model

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(
                status_code=503,
                detail="IRR model not trained yet"
            )
        _model = joblib.load(MODEL_PATH)

    return _model


class IRRPredictor:

    @staticmethod
    async def predict(ticket_id: str):
        db = get_database()

        ticket = await db.tickets.find_one({"_id": ObjectId(ticket_id)})

        if not ticket:
            return {"error": "Ticket not found"}
        
        if ticket.get("irr_label") is not None:
            return {
                "message": "Ticket already labeled",
                "irr_label": ticket["irr_label"]
            }

        model = get_model()

        features = await FeatureService.extract_features(ticket_id)
        X = [list(features.values())]

        prob = model.predict_proba(X)[0][1]

        return {
            "predicted_irr": int(prob >= 0.5),
            "confidence": round(prob, 3),
            "features": features
        }
