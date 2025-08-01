from fastapi import FastAPI, Request
from api import auth, users, patients, temperatures, treatments
from core.config import settings
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="CryoMind API")

# Rutas agrupadas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(patients.router, prefix="/patients", tags=["patients"])
# app.include_router(temperatures.router, prefix="/temperatures", tags=["temperatures"])
# app.include_router(treatments.router, prefix="/treatments", tags=["treatments"])

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})