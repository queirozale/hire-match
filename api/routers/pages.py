from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="api/templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "home page"})


@router.get("/about", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request, "message": "about page"})


@router.get("/login", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": "login page"})


@router.get("/form", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request, "message": "form page"})


@router.get("/form-company", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("cadastroEmpresa.html", {"request": request, "message": "form company page"})


@router.get("/form-candidate", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("cadastroCandidato.html", {"request": request, "message": "form candidate page"})


@router.get("/profile-candidate", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("perfilCandidato.html", {"request": request, "message": "profile candidate page"})


@router.get("/profile-company", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("perfilEmpresa.html", {"request": request, "message": "profile company page"})

