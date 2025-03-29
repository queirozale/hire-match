from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class ExperienceSchema(BaseModel):
    company: str
    position: str
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None

class EducationSchema(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_year: int
    end_year: int

class ResumeSchema(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str]
    experience: List[ExperienceSchema]
    education: List[EducationSchema]
    certifications: Optional[List[str]] = []
    projects: Optional[List[str]] = []

    class Config:
        json_encoders = {
            ObjectId: str
        }

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