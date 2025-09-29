import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # Module path to FastAPI instance
        host="0.0.0.0",  # or "0.0.0.0" to be reachable externally
        port=8000,
        reload=True,  # Auto-reload on code changes (dev only)
    )
