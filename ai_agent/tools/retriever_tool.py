from langchain.tools.retriever import create_retriever_tool
from ai_agent.tools.vectorestore import load_retriever


# Crea una herramienta a partir del retriever
retriever_tool = create_retriever_tool(
    load_retriever(),
    name="info_retriever",
    description="Busca información en el pdf para responder a las preguntas de los trabajadores."
)