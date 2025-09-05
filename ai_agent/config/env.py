from dotenv import load_dotenv, find_dotenv
import os

# Carga de variables de entorno
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# LangSmith para trazabilidad en LangChain / LangGraph
LANGSMITH_TRACING=os.getenv("LANGSMITH_TRACING")
LANGSMITH_ENDPOINT=os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY=os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT=os.getenv("LANGSMITH_PROJECT")

# OpenAI LLM general
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Modelo y clave para agente Amparo
# AMPARO_MODEL=os.getenv("AMPARO_MODEL")
# AMPARO_API_KEY=os.getenv("AMPARO_API_KEY")

# Embeddings
EMBEDDINGS_MODEL=os.getenv("EMBEDDINGS_MODEL")

# Path base de datos
DB_PATH ="OPMS/settings/DATABASES"
PDF_PATH = "ai_agent/data/guia_condominio_altavista_completa.pdf"
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "ai_agent/vectorstore/index")
DB_PATH_CHECKPOINTER = "ai_agent/persistence/memoria_chat-db"
