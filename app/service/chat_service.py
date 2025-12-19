from sqlalchemy.orm import Session

from app.agent.graph import gen_graph
from app.agent.state import State
from app.db.database import SessionLocal
from app.schema.chat import MessageRequestSchema, MessageResponseSchema
from datetime import datetime
import uuid


class ChatService:

    def __init__(self):
        self.db: Session = SessionLocal()
        self.agent = gen_graph()
        self.chat_history = {}

    async def send_message(self, request: MessageRequestSchema) -> MessageResponseSchema:

        session_id = request.session_id or str(uuid.uuid4())


        if session_id not in self.chat_history:
            self.chat_history[session_id] = []

        user_msg = request.message.lower().strip()
        print(user_msg)

        initialState : State = {"message" : [],
                                "user_query" : user_msg,
                                "response":""}

        agent_state = await self.agent.ainvoke(initialState)

        reply = agent_state["response"]
        print(reply)
        return MessageResponseSchema(
            message=reply,
            session_id=session_id,
            timestamp=datetime.now()
        )


def get_chat_service():
    return ChatService()
