from enum import Enum


class nodes(str,Enum):

    CHATBOT_NODE = "chatbot_node"
    CALLING_NODE = "calling_node"
    DB_NODE = "db_node"
    EXECUTE_DATABASE_QUERY_NODE = "execute_database_query"