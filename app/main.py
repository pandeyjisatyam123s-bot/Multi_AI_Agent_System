from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from .routes import router

app = FastAPI(
    title="Multi-Agent Research System API",
    description="API for managing research tasks with LangGraph and Agents",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Serve the React frontend in production
dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web", "dist"))

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # If it's a file request that exists (e.g. /assets/index.js)
    file_path = os.path.join(dist_dir, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Otherwise, return index.html for React Router handling
    index_path = os.path.join(dist_dir, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    
    return {"error": "Frontend not built. Please run 'npm run build' in the web/ directory."}
