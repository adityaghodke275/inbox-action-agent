from fastapi import FastAPI
from app.api.emails import router as email_router
from app.api.memory import router as memory_router
from app.api.responses import router as response_router

app = FastAPI(
    title="Inbox Action Agent",
    description="AI-powered email inbox action and automation agent",
    version="1.0.0",
)

app.include_router(email_router) 
app.include_router(memory_router)
app.include_router(response_router)

@app.get("/")
def root():
    return {
        "service": "Inbox Action Agent",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Inbox Action Agent",
    }