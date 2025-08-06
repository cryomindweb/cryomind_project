from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="../frontend/templates")

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/404", response_class=HTMLResponse)
async def not_found_page(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})

@router.get("/403", response_class=HTMLResponse)
async def forbidden_page(request: Request):
    return templates.TemplateResponse("403.html", {"request": request})

@router.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@router.get("/medico", response_class=HTMLResponse)
async def user_page(request: Request):
    return templates.TemplateResponse("pacientes.html", {"request": request})
