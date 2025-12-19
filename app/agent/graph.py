import logging
from langgraph.graph import StateGraph, START, END

from app.agent.node.execute_database_query import execute_database_query
from app.agent.node.calling_node import calling_node
from app.agent.node.chatbot_node import chatbot_node
from app.agent.node.db_node import db_node
from app.agent.state import State
from app.enums.nodes import nodes


def gen_graph():

    logging.info("Generating graph")

    workflow = StateGraph(State)
    workflow.add_node(nodes.CHATBOT_NODE, chatbot_node)
    workflow.add_node(nodes.CALLING_NODE, calling_node)
    workflow.add_node(nodes.DB_NODE, db_node)
    workflow.add_node(nodes.EXECUTE_DATABASE_QUERY_NODE, execute_database_query)

    def route_after_calling_node (state: State) -> str:
        decision = state.get("decision")

        if decision == "database":
            return nodes.DB_NODE
        else:

            return nodes.CHATBOT_NODE

    workflow.set_entry_point(nodes.CALLING_NODE)

    workflow.add_conditional_edges(
        nodes.CALLING_NODE,
        route_after_calling_node,
        {
            nodes.DB_NODE: nodes.CHATBOT_NODE,
            nodes.CHATBOT_NODE: nodes.CHATBOT_NODE,
        }
    )

    workflow.add_edge(nodes.CHATBOT_NODE, END)
    workflow.add_edge(nodes.DB_NODE, nodes.EXECUTE_DATABASE_QUERY_NODE)
    workflow.add_edge(nodes.EXECUTE_DATABASE_QUERY_NODE, END)

    return workflow.compile()




