import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from config.settings import settings

def get_llm(provider: str = None, model_name: str = None):
    load_dotenv(override=True)
    provider = provider or settings.llm_provider
    
    openai_key = os.getenv("OPENAI_API_KEY") or settings.openai_api_key or "sk-placeholder-key-set-in-env"
    gemini_key = os.getenv("GEMINI_API_KEY") or settings.gemini_api_key or "placeholder-key-set-in-env"
    groq_key = os.getenv("GROQ_API_KEY") or settings.groq_api_key or "gsk_placeholder-key-set-in-env"

    
    if provider == "groq":
        model_name = model_name or settings.llm_model or "qwen/qwen3.8-27b"
        return ChatGroq(model=model_name, api_key=groq_key, max_tokens=800)



    elif provider == "openai":
        model_name = model_name or "gpt-4o-mini"
        return ChatOpenAI(model=model_name, api_key=openai_key)
    elif provider == "gemini":
        model_name = model_name or "gemini-1.5-flash"
        return ChatGoogleGenerativeAI(model=model_name, google_api_key=gemini_key)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


