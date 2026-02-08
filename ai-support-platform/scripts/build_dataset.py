import asyncio
import pandas as pd
from app.core.database import get_database, init_db, close_db
from app.services.feature_service import FeatureService

async def build():
    await init_db()  

    db = get_database()
    rows = []

    async for ticket in db.tickets.find({"irr_label": {"$ne": None}}):
        features = await FeatureService.extract_features(str(ticket["_id"]))
        features["irr_label"] = ticket["irr_label"]
        rows.append(features)

    if not rows:
        print("No labeled tickets found. Dataset not created.")
        await close_db()
        return

    df = pd.DataFrame(rows)
    df.to_csv("irr_dataset.csv", index=False)
    print("Dataset saved:", df.shape)

    await close_db()

asyncio.run(build())
