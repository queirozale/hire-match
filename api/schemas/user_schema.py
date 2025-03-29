from pydantic import BaseModel, EmailStr
from typing import Optional

# Pydantic schema for user
class UserSchema(BaseModel):
    email: EmailStr
    category: str  # Either "recruiter" or "candidate"
    password: str
