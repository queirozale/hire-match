from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from api.utils.pass_hash import verify_password

load_dotenv()

router = APIRouter()

# Secret Key for JWT Token
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"

# OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "local"
COLLECTION_NAME = "users"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

class UserLogin(BaseModel):
    username: str
    password: str

def create_access_token(data: dict):
    """Generate a JWT token"""
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """User login route"""
    user = await collection.find_one({"email": form_data.username})

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user["email"]})

    return {"access_token": token, "token_type": "bearer"}
