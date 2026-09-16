from pydantic import BaseModel

class ResearchResponse(BaseModel):
    task_id: str
    status: str
    message: str
