from fastapi import FastAPI
from api.routers import login, resumes, users
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Secret Key for JWT Token
SECRET_KEY = os.getenv("SECRET_KEY")
app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(login.router, tags=["Login"])

