from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
import sqlite3
from ai_agent.config.env import DB_PATH_CHECKPOINTER

conn = sqlite3.connect(DB_PATH_CHECKPOINTER, check_same_thread=False)
checkpointer = SqliteSaver(conn, serde=JsonPlusSerializer(pickle_fallback=True))