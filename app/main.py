from fastapi import FastAPI
from routers import resumes, users  

app = FastAPI()

# Include the resumes router
app.include_router(users.router, prefix="/resumes", tags=["Resumes"])
app.include_router(users.router, prefix="/users", tags=["Users"])

