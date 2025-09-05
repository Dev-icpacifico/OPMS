from langchain_openai import ChatOpenAI
from typing import Optional
from ai_agent.config.agents import LLMType
from ai_agent.config.env import (
    LANGSMITH_TRACING,
    LANGSMITH_ENDPOINT,
    LANGSMITH_API_KEY,
    LANGSMITH_PROJECT,
    OPENAI_API_KEY,
    EMBEDDINGS_MODEL,
)

# llm = ChatOpenAI(model="gpt-4o")
def create_openai_llm(
        model:str,
        base_url:Optional[str] = None,
        api_key:Optional[str] = None,
        temperature : float = 0.0,
        **kwargs,
)->ChatOpenAI:
    """
    Crate a ChatOpenAI instance with the specified configuration.
    :param model:
    :param base_url:
    :param api_key:
    :param temperature:
    :param kwargs:
    :return:
    """
    # Solo incluya base_url en los argumentos si no es Ninguno o está vacío
    llm_kwargs = {"model":model, "temperature":temperature, **kwargs}

    if base_url: # Esto manejará Ninguno o cadena vacía
        llm_kwargs["base_url"] = base_url
    if api_key: # Esto manejará Ninguno o cadena vacía
        llm_kwargs["api_key"] = api_key

    return ChatOpenAI(**llm_kwargs)

# Cache para instancias de LLM
_llm_cache: dict[LLMType, ChatOpenAI] = {}
def get_llm_by_type(llm_type: LLMType) -> ChatOpenAI:
    """
    Obtener la instancia de LLM por tipo. Devuelve la instancia en caché si está disponible.
    """

    if llm_type in _llm_cache:
        return _llm_cache[llm_type]

    if llm_type == "reasoning":
        llm = create_openai_llm(
            model="gpt-4o",
            api_key=OPENAI_API_KEY,
        )
    elif llm_type == "basic":
        llm = create_openai_llm(
            model="gpt-4o",
            api_key=OPENAI_API_KEY,
        )
    else:
        raise ValueError(f"Unknown LLM type {llm_type}")

    _llm_cache[llm_type] = llm
    return llm

# Inicializar LLM para diferentes propósitos: ahora se almacenarán en caché

basic_llm = get_llm_by_type("basic")
reasoning_llm = get_llm_by_type("reasoning")
