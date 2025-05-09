import random
from datetime import datetime, timedelta
from mongoengine import connect

from api.database.models.resume_model import Resume

POP_SIZE = 30

def random_date(start_date: datetime, end_date: datetime):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

brazilian_names = [
    "Ana Silva", "João Santos", "Maria Oliveira", "Pedro Souza", "Lucas Pereira",
    "Julia Costa", "Gabriel Rodrigues", "Beatriz Almeida", "Rafael Carvalho", "Amanda Gomes",
    "Vinicius Fernandes", "Larissa Martins", "Gustavo Rocha", "Carolina Barbosa", "Thiago Castro",
    "Isabela Nunes", "Felipe Azevedo", "Renata Correia", "Eduardo Ribeiro", "Camila Lima",
    "Matheus Santos", "Fernanda Oliveira", "Ricardo Souza", "Patrícia Pereira", "Leonardo Costa",
    "Juliana Rodrigues", "Marcelo Almeida", "Letícia Carvalho", "Diego Gomes", "Vanessa Fernandes"
]

brazilian_phones = ["+55 11 98765-4321", "+55 21 91234-5678", "+55 31 99999-8888", "+55 41 95555-7777", "+55 51 92222-3333"]

companies = ["TechCorp Brasil", "DevSolutions BR", "InovateTech Brasil", "WebLabs Brasil", "SoftCo Brasil"]
positions = ["Engenheiro(a) de Software", "Cientista de Dados", "Engenheiro(a) DevOps", "Desenvolvedor(a) Frontend", "Desenvolvedor(a) Backend"]
skills = ["Python", "MongoDB", "Docker", "JavaScript", "AWS", "Kubernetes", "SQL", "Java", "C++", "React"]
certifications = ["AWS Certified Developer", "Oracle Certified Java Programmer", "Certified Kubernetes Administrator"]
projects = ["Projeto Alfa", "Projeto Beta", "Projeto Gama", "Projeto Delta", "Projeto Épsilon"]

email_counter = 0  # Keep track of generated emails

def create_random_resume():
    global email_counter  # Access the global counter
    name = random.choice(brazilian_names)
    base_email = name.lower().replace(' ', '.')
    email = f"{base_email}_{email_counter}@email.com"  # Add a unique identifier
    email_counter += 1
    phone = random.choice(brazilian_phones)
    summary = "Resumo profissional genérico."
    experience = [{
        "company": random.choice(companies),
        "position": random.choice(positions),
        "start_date": random_date(datetime(2015, 1, 1), datetime(2020, 1, 1)).strftime("%Y-%m-%d"),
        "end_date": random_date(datetime(2020, 1, 1), datetime(2025, 1, 1)).strftime("%Y-%m-%d"),
        "description": "Descrição genérica da experiência."
    }]
    education = [{
        "institution": "Universidade Genérica",
        "degree": random.choice(["BSc Ciência da Computação", "BSc Tecnologia da Informação", "MSc Engenharia de Software"]),
        "field_of_study": random.choice(["Ciência da Computação", "Tecnologia da Informação", "Engenharia de Software"]),
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
