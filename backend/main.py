from fastapi import FastAPI, Request
from api import auth, users, patients, temperatures, treatments
from views import pages as pages_router
from core.config import settings
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="CryoMind API")

# Rutas agrupadas
app.include_router(pages_router.router) # type: ignore
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(temperatures.router, prefix="/temperatures", tags=["temperatures"])
app.include_router(treatments.router, prefix="/treatments", tags=["treatments"])

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


