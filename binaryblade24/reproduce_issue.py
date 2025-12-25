import urllib.request
import urllib.error
import json
import sys

def test_registration():
    url = "http://127.0.0.1:8000/api/auth/register/"
    data = {
        "username": "testuser_repro_v2",
        "first_name": "Test",
        "last_name": "User",
        "country_origin": "ZA",
        "identity_number": "1234567890",
        "phone_number": "1234567890",
        "email": "testuser_repro_v2@example.com",
        "password": "password123",
        "roles": ["FREELANCER"]
    }
    
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
    
    print(f"Attempting to register user at {url}...")
    print(f"Payload: {json.dumps(data, indent=2)}")
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Status Code: {response.getcode()}")
            print("Response Body:")
            print(response.read().decode('utf-8'))
            print("\nSUCCESS: Registration successful.")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        print("Error Body:")
        print(e.read().decode('utf-8'))
        print("\nFAILURE: Registration failed.")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        print("\nFAILURE: Could not connect to server.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nFAILURE: Unexpected error.")

if __name__ == "__main__":
    test_registration()
