import os
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Usamos la misma variable de entorno ya configurada
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

def ejecutar_agente_auditor(consulta: str):
    """
    Agente configurado para actuar como un experto en seguridad.
    """
    # 1. Conectar  cerebro local (Ollama)
    llm = ChatOllama(base_url=OLLAMA_BASE_URL, model="qwen2.5:7b")
    
    # 2. Definir el comportamiento del Agente (System Prompt estricto)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un Agente de IA corporativo especializado en ciberseguridad. Tu trabajo es analizar la consulta del usuario y devolver SIEMPRE una respuesta estructurada con: 1) Riesgo detectado, 2) Solución propuesta, y 3) Nivel de criticidad."),
        ("user", "{consulta}")
    ])
    
    # 3. Crear (Pipeline) del agente
    agente = prompt | llm
    
    # 4. Ejecutar el agente
    respuesta = agente.invoke({"consulta": consulta})
    return respuesta.content
