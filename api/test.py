import requests

url = "http://127.0.0.1:8000/auth"

data = {
    "username": "usuario@email.com",  # OAuth2 expects "username", even if it's an email
    "password": "abc123"
}

response = requests.post(url, data=data)

print(response.json())  # Should return {"access_token": "...", "token_type": "bearer"}
