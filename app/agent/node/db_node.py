from fastapi import logger
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.agent.state import State
from app.db.database import get_table_info


def db_node(state: State )-> State:
    from app.core.config import settings
    chatGPT = ChatOpenAI(model_name="gpt-5-nano", temperature=0,openai_api_key=settings.OPENAI_API_KEY)

    db_info = get_table_info()

    system_message = f"""
    
    You are an intelligent SQL query generator that converts user questions into executable MySQL queries.
    Here is the database schema:{db_info}
    Your task:
    Generate **only a valid MySQL SELECT, INSERT, UPDATE, or DELETE query** based on the user’s natural language question.

    Rules:
    1. Always reference the database and table as `flight_update.flight_tracer`.
    2. Return **only the SQL query** — no explanations, no formatting, no comments.
    3. Do not include backticks or markdown formatting.
    4. If user input is unclear, make the best logical assumption and still return a valid SQL query.
    5. Use `LIKE` for partial text matches and `BETWEEN` for date/time ranges when applicable.
    6. Assume datetime fields (`departure`, `arrival`) are in standard 'YYYY-MM-DD HH:MM:SS' format.
    7. If the question requests data filtering (e.g., "flights from Colombo to Dubai"), use appropriate `WHERE` conditions.

    Example behaviors:
    User: "Show all flights from Colombo to Dubai"
    → SELECT * FROM flight_update.flight_tracer WHERE origin='Colombo' AND destination='Dubai';

    User: "Find flights cheaper than 5000"
    → SELECT * FROM flight_update.flight_tracer WHERE ticket_price < 5000;

    User: "Update ticket price of flight EK401 to 7500"
    → UPDATE flight_update.flight_tracer SET ticket_price=7500 WHERE flight_number='EK401';

    User: "Delete flight with number UL104"
    → DELETE FROM flight_update.flight_tracer WHERE flight_number='UL104';

Respond with **only** the SQL query — nothing else.
    
    """

    user_message = state.get("user_query", "")

    messages_LLM = [SystemMessage(content=system_message),HumanMessage(content=user_message)]
    response = chatGPT.invoke(messages_LLM)

    state["sql_query"] = response.content
    logger.info(response.content)
    return state

