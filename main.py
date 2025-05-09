from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api.routers import auth, resumes, users, pages
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Secret Key for JWT Token
SECRET_KEY = os.getenv("SECRET_KEY")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://127.0.0.1:8000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Jinja2 templates setup
templates = Jinja2Templates(directory="api/templates")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(pages.router, tags=["Pages"])

