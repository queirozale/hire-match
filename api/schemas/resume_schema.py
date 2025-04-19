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
    education: List[EducationSchema]
    experience: Optional[List[ExperienceSchema]] = []
    certifications: Optional[List[str]] = []
    projects: Optional[List[str]] = []

    class Config:
        json_encoders = {
            ObjectId: str
        }