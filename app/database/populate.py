import random
from faker import Faker
from datetime import datetime, timedelta
from mongoengine import connect

from models.resume import Resume


fake = Faker()
POP_SIZE = 30

def random_date(start_date: datetime, end_date: datetime):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


companies = ["TechCorp", "DevSolutions", "InnovateTech", "WebLabs", "SoftCo"]
positions = ["Software Engineer", "Data Scientist", "DevOps Engineer", "Frontend Developer", "Backend Developer"]
skills = ["Python", "MongoDB", "Docker", "JavaScript", "AWS", "Kubernetes", "SQL", "Java", "C++", "React"]
certifications = ["AWS Certified Developer", "Oracle Certified Java Programmer", "Certified Kubernetes Administrator"]
projects = ["Project A", "Project B", "Project C", "Project D", "Project E"]


def create_random_resume():
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    summary = fake.sentence(nb_words=8)
    experience = [{
        "company": random.choice(companies),
        "position": random.choice(positions),
        "start_date": random_date(datetime(2015, 1, 1), datetime(2020, 1, 1)).strftime("%Y-%m-%d"),
        "end_date": random_date(datetime(2020, 1, 1), datetime(2025, 1, 1)).strftime("%Y-%m-%d"),
        "description": fake.sentence(nb_words=12)
    }]
    education = [{
        "institution": fake.company(),
        "degree": random.choice(["BSc Computer Science", "BSc Information Technology", "MSc Software Engineering"]),
        "field_of_study": random.choice(["Computer Science", "Information Technology", "Software Engineering"]),
        "start_year": random.randint(2005, 2015),
        "end_year": random.randint(2010, 2020)
    }]
    certifications_list = random.sample(certifications, random.randint(1, 3))
    projects_list = random.sample(projects, random.randint(1, 3))

    resume = Resume(
        name=name,
        email=email,
        phone=phone,
        summary=summary,
        skills=random.sample(skills, random.randint(3, 6)),
        experience=experience,
        education=education,
        certifications=certifications_list,
        projects=projects_list
    )

    return resume

resumes = [create_random_resume() for _ in range(POP_SIZE)]

connect('local', host='localhost', port=27017)
for resume in resumes:
    resume.save()
