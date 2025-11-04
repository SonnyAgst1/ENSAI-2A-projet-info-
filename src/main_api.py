from fastapi import FastAPI
from api.routers import router as activites_router

app = FastAPI()

app.include_router(activites_router)
