"""
BoxTech FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="BoxTech API",
    description="AI Boxing Training Analysis System",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from backend.api.health import router as health_router  # noqa: E402
from backend.api.videos import router as videos_router  # noqa: E402

app.include_router(health_router)
app.include_router(videos_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to BoxTech API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Run using the fully-qualified module path so it works from the repo root
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
