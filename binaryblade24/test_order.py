import requests
import json

# Test order creation
url = "http://127.0.0.1:8000/api/orders/orders/"

# You'll need to replace this with a valid token
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_TOKEN_HERE"
}

data = {
    "items_data": [
        {
            "project_id": 1,  # Replace with actual project ID
            "tier": "SIMPLE"
        }
    ]
}

print("Testing order creation...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")

# Uncomment to actually test:
# response = requests.post(url, json=data, headers=headers)
# print(f"Status: {response.status_code}")
# print(f"Response: {response.json()}")
