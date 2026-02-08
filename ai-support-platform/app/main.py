from fastapi import FastAPI
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routes import health, products, orders, tickets, conversations

app = FastAPI(title="AI Support Platform")

@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

app.include_router(health.router)
app.include_router(products.router, prefix="/products")
app.include_router(orders.router, prefix="/orders")
app.include_router(tickets.router, prefix="/tickets")
app.include_router(conversations.router, prefix="/conversations")

