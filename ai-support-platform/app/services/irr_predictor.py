import os
import joblib
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
        model = get_model()

        features = await FeatureService.extract_features(ticket_id)
        X = [list(features.values())]

        prob = model.predict_proba(X)[0][1]

        return {
            "predicted_irr": int(prob >= 0.5),
            "confidence": round(prob, 3),
            "features": features
        }
