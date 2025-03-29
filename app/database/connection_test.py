from mongoengine import connect
from datetime import datetime
from models.resume import Resume, Experience, Education  # Import your model

# Connect to MongoDB (adjust the URI as needed)
connect('local', host='localhost', port=27017)

# Create an Experience object
exp = Experience(
    company="TechCorp",
    position="Software Engineer",
    start_date=datetime(2020, 6, 1),
    end_date=datetime(2023, 5, 30),
    description="Developed software solutions and led the backend team."
)

# Create an Education object
edu = Education(
    institution="University of Example",
    degree="BSc Computer Science",
    field_of_study="Computer Science",
    start_year=2016,
    end_year=2020
)

# Create a Resume object
resume = Resume(
    name="John Doe",
    email="john.doe@example.com",
    phone="123-456-7890",
    summary="Experienced Software Engineer with a strong background in backend development.",
    skills=["Python", "Java", "MongoDB", "Docker"],
    experience=[exp],
    education=[edu],
    certifications=["AWS Certified Developer", "Oracle Certified Java Programmer"],
    projects=["Project A", "Project B"]
)

# Save the Resume object to MongoDB
resume.save()

# # Query the database (for example, get the first resume)
# retrieved_resume = Resume.objects.first()
# print(retrieved_resume.name)
# print(retrieved_resume.experience[0].company)

# # Update a resume (e.g., update the phone number)
# retrieved_resume.update(set__phone="987-654-3210")

# # Delete a resume (e.g., by email)
# Resume.objects(email="john.doe@example.com").delete()
