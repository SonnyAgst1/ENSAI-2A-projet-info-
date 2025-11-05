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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes API
app.include_router(activites_router, prefix="/api")

# ⭐ SERVIR LA PAGE HTML
@app.get("/")
def read_frontend():
    frontend_path = os.path.join(
        os.path.dirname(__file__), 
        "..", 
        "frontend", 
        "index.html"
    )
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Frontend non trouvé", "docs": "/docs"}

@app.get("/api")
def api_info():
    return {"status": "online", "docs": "/docs"}