from fastapi import FastAPI
from api.routers import activites

app = FastAPI(title="Sport App API")
app.include_router(activites.router)
