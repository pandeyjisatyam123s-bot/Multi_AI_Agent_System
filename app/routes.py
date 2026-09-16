from fastapi import APIRouter
from schemas.request import ResearchRequest
from schemas.response import ResearchResponse
from graph.workflow import create_workflow
from langchain_core.messages import HumanMessage

router = APIRouter()

app_workflow = create_workflow()

@router.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest):
    initial_state = {
        "messages": [HumanMessage(content=f"Research topic: {request.topic}")],
        "topic": request.topic
    }
    
    try:
        app_workflow = create_workflow()
        final_state = app_workflow.invoke(initial_state)
        final_report = final_state.get("final_report")
        if not final_report:
            for msg in reversed(final_state.get("messages", [])):
                if getattr(msg, "content", None) and getattr(msg, "name", "") in ["Writer", "Search"]:
                    final_report = msg.content
                    break
        final_report = final_report or "No report was generated."


        
        return ResearchResponse(
            task_id="graph-run",
            status="completed",
            message=final_report
        )
    except Exception as e:
        return ResearchResponse(
            task_id="graph-run",
            status="error",
            message=str(e)
        )
