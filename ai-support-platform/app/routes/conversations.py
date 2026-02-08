from fastapi import APIRouter
from typing import List
from app.models.conversation import Conversation
from app.models.message import Message, MessageInput
from app.services.conversation_service import ConversationService
from app.core.database import get_database

router = APIRouter()

@router.post("/", response_model=Conversation)
async def start_conversation(conversation: Conversation):
    return await ConversationService.start_conversation(conversation)

@router.post("/{conversation_id}/messages", response_model=Message)
async def add_message(conversation_id: str, message_input: MessageInput):
    message = Message(
        conversation_id=conversation_id,
        ticket_id=message_input.ticket_id,
        sender_type=message_input.sender_type,
        sender_id=message_input.sender_id,
        text=message_input.text,
        confidence=message_input.confidence,
        intent=message_input.intent,
        entities=message_input.entities,
        is_correction=message_input.is_correction,
        is_escalation_request=message_input.is_escalation_request
    )
    return await ConversationService.add_message(message)

@router.get("/{conversation_id}/messages", response_model=List[Message])
async def get_messages(conversation_id: str):
    db = get_database()
    messages = []
    async for m in db.messages.find({"conversation_id": conversation_id}):
        m["_id"] = str(m["_id"])
        messages.append(m)
    return messages
