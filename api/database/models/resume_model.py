from mongoengine import Document, StringField, ListField, EmbeddedDocument, EmbeddedDocumentField, DateField, IntField

class Experience(EmbeddedDocument):
    company = StringField(required=True)
    position = StringField(required=True)
    start_date = DateField(required=True)
    end_date = DateField()
    description = StringField()

class Education(EmbeddedDocument):
    institution = StringField(required=True)
    degree = StringField(required=True)
    field_of_study = StringField()
    start_year = IntField()
    end_year = IntField()

class Resume(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone = StringField()
    summary = StringField()
    skills = ListField(StringField())
    experience = ListField(EmbeddedDocumentField(Experience))
    education = ListField(EmbeddedDocumentField(Education))
    certifications = ListField(StringField())
    projects = ListField(StringField())

    meta = {'collection': 'resumes'}

class Position(Document):
    title = StringField(required=True)
    company = StringField(required=True)
    location = StringField()
    description = StringField()