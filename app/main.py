from fastapi import FastAPI, HTTPException, Body, Query
from pydantic import BaseModel
from mongoengine import connect
from datetime import datetime
from typing import List, Optional
import os
from bson import ObjectId

from database.models.resume import Resume, Education, Experience
from schemas.resume import ResumeSchema, EducationSchema, ExperienceSchema, resume_helper
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# MongoDB connection URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "local"
COLLECTION_NAME = "resumes"

# MongoDB client setup
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.get("/resumes/", response_model=List[ResumeSchema])
async def get_resumes(skill: Optional[str] = Query(None, min_length=2, max_length=50)):
    query = {}

    if skill:  # If skill is provided, filter resumes that contain the skill
        query["skills"] = {"$in": [skill]}  # MongoDB query to search for skill in skills array

    resumes_cursor = collection.find(query)

    # Convert the MongoDB cursor to a list of documents
    resumes_list = [resume_helper(resume) async for resume in resumes_cursor]

    return resumes_list

# Create a resume
@app.post("/resumes/", response_model=ResumeSchema)
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
@app.get("/resumes/{email}", response_model=ResumeSchema)
async def get_resume(email: str):
    resume = await collection.find_one({"email": email})
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume_helper(resume)

# Update a resume by email
@app.put("/resumes/{email}", response_model=None)
async def update_resume(email: str, resume: ResumeSchema):
    resume_dict = resume.dict(exclude_unset=True)  # Exclude unset fields to update only provided fields

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
@app.delete("/resumes/{email}")
async def delete_resume(email: str):
    result = await collection.delete_one({"email": email})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return {"detail": f"Resume with email {email} has been deleted."}

