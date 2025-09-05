import os

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ai_agent.config.env import PDF_PATH, FAISS_INDEX_PATH, EMBEDDINGS_MODEL


def load_retriever():
    # Paso 1: Inicializar embeddings
    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)

    # Paso 2: Si existe el índice FAISS, lo cargamos
    if os.path.exists(FAISS_INDEX_PATH):
        vectorstore = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True  # necesario si el índice fue guardado en local
        )
    else:
        # Paso 3: Si no existe, construir el índice desde el PDF
        loader = PyPDFLoader(PDF_PATH)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(splits, embeddings)
        vectorstore.save_local(FAISS_INDEX_PATH)

    # Paso 4: Devolver el retriever
    return vectorstore.as_retriever(search_kwargs={"k": 10})
