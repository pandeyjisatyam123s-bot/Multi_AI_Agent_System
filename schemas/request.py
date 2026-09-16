from pydantic import BaseModel

class ResearchRequest(BaseModel):
    topic: str
    depth: str = "comprehensive"
