"""
Top-level ASGI entrypoint for Uvicorn.
This allows running: `uvicorn main:app --reload` from the repo root.
"""
from backend.main import app  # re-export FastAPI app

# Optional: enable `python main.py` for local runs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
