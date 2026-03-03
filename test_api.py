import requests
import json

url = "http://127.0.0.1:8007/analyze-text"
payload = {
    "text": "Bu kurs hayatımı değiştirdi!",
    "provider": "gemini"
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
