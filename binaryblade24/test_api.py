import requests
import json

try:
    response = requests.get('http://127.0.0.1:8000/api/projects/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total items: {len(data)}")
        for item in data:
            print(f"Title: {item.get('title')}, Type: {item.get('project_type')}, Status: {item.get('status')}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
