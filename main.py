from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Dummy Backend API",
    description="A simple dummy backend server built with FastAPI",
    version="1.0.0"
)

# Include all routes from routes.py
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

