from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from api.routers import router as activites_router
from database import Base, engine
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Application Sportive API",
    version="1.0.0"
)


# Routes API
app.include_router(activites_router, prefix="/api")

@app.get("/api")
def api_info():
    return {"status": "online", "docs": "/docs"}