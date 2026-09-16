from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    openai_api_key: str = ""
    gemini_api_key: str = ""
    tavily_api_key: str = ""
    groq_api_key: str = ""

    llm_provider: str = "groq"
    llm_model: str = "llama3-8b-8192"



    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
