from mongoengine import Document, StringField, EmailField

# MongoEngine model for user
class User(Document):
    email = EmailField(required=True, unique=True)
    category = StringField(required=True, choices=["recruiter", "candidate"])
    password = StringField(required=True)
    
    meta = {
        "collection": "users"  # The MongoDB collection name
    }
