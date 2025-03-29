from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import BaseModel
from mongoengine import connect
from datetime import datetime
from typing import List, Optional
import os
from bson import ObjectId

from database.models.resume import Resume, Education, Experience
from schemas.resume import ResumeSchema, EducationSchema, ExperienceSchema
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

# MongoDB connection URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "local"
COLLECTION_NAME = "resumes"

# MongoDB client setup
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def resume_helper(resume: ResumeSchema) -> dict:
    # Map MongoDB document fields to ResumeSchema
    return {
        "name": resume["name"],
        "email": resume["email"],
        "phone": resume.get("phone"),
        "summary": resume.get("summary"),
        "skills": resume.get("skills", []),
        "experience": [
            ExperienceSchema(**exp) for exp in resume.get("experience", [])
        ],
        "education": [
            EducationSchema(**edu) for edu in resume.get("education", [])
        ],
        "certifications": resume.get("certifications", []),
        "projects": resume.get("projects", []),
    }


@router.get("/", response_model=List[ResumeSchema])
async def get_resumes(skill: Optional[str] = Query(None, min_length=2, max_length=50)):
    query = {}

    if skill:  # If skill is provided, filter resumes that contain the skill
        query["skills"] = {"$in": [skill]}  # MongoDB query to search for skill in skills array

    resumes_cursor = collection.find(query)

    # Convert the MongoDB cursor to a list of documents
    resumes_list = [resume_helper(resume) async for resume in resumes_cursor]

    return resumes_list

# Create a resume
@router.post("/", response_model=ResumeSchema)
async def create_resume(resume: ResumeSchema):
    try:
        resume_dict = resume.model_dump()
        
        # Insert into the collection
        resume_dict["_id"] = ObjectId()  # Manually set _id as ObjectId for MongoDB
        result = await collection.insert_one(resume_dict)
        
        # Fetch the created resume
        created_resume = await collection.find_one({"_id": result.inserted_id})
        
        return resume_helper(created_resume)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating resume: {e}")

# Read a resume by email
@router.get("/{email}", response_model=ResumeSchema)
async def get_resume(email: str):
    resume = await collection.find_one({"email": email})
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume_helper(resume)

# Update a resume by email
@router.put("/{email}", response_model=None)
async def update_resume(email: str, resume: ResumeSchema):
    resume_dict = resume.model_dump(exclude_unset=True)  # Exclude unset fields to update only provided fields

    # Perform the update
    result = await collection.update_one(
        {"email": email},
        {"$set": resume_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")

    # If update is successful, return a success message with status 200
    return {"detail": "Resume updated successfully"}



# Delete a resume by email
@router.delete("/{email}")
async def delete_resume(email: str):
    result = await collection.delete_one({"email": email})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return {"detail": f"Resume with email {email} has been deleted."}

