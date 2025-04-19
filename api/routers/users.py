from fastapi import APIRouter, HTTPException
from pydantic import EmailStr
from typing import List
from mongoengine.errors import NotUniqueError
from api.schemas.user_schema import UserSchema
from api.database.models.user_model import User
import os
from motor.motor_asyncio import AsyncIOMotorClient

from api.utils.pass_hash import hash_password

router = APIRouter()

# MongoDB connection URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "local"
COLLECTION_NAME = "users"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Helper function to convert MongoDB document to Python dict
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "category": user["category"],
        "password": user["password"],
    }


# Create a new user
@router.post("/", response_model=UserSchema)
async def create_user(user: UserSchema):
    try:
        # Convert Pydantic model to dict for insertion into MongoDB
        user_dict = user.model_dump()
        user_dict['password'] = hash_password(user_dict['password'])
        result = await collection.insert_one(user_dict)
        created_user = await collection.find_one({"_id": result.inserted_id})
        return user_helper(created_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {e}")

# Get a user by email
@router.get("/{email}", response_model=UserSchema)
async def get_user(email: str):
    user = await collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)

# Update a user by email
@router.put("/{email}", response_model=None)
async def update_user(email: str, user: UserSchema):
    user_dict = user.dict(exclude_unset=True)

    result = await collection.update_one(
        {"email": email},
        {"$set": user_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": "User updated successfully"}

# Delete a user by email
@router.delete("/{email}")
async def delete_user(email: str):
    result = await collection.delete_one({"email": email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": f"User with email {email} has been deleted."}