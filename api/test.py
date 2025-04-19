import requests

url = "http://127.0.0.1:8000/login"

data = {
    "username": "ale@gmail.com",  # OAuth2 expects "username", even if it's an email
    "password": "123456"
}

response = requests.post(url, data=data)

print(response.json())  # Should return {"access_token": "...", "token_type": "bearer"}
