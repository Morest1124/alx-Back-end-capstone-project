import requests
import json
import jwt

BASE = "https://binaryblade24-api.onrender.com"

with open('mock_data.json','r') as f:
    data = json.load(f)

users = data.get('users', [])

results = []

for u in users:
    email = u.get('email')
    password = u.get('password')
    username = u.get('username')
    try:
        r = requests.post(f"{BASE}/api/auth/login/", json={"email": email, "password": password}, timeout=10)
        if r.status_code == 200:
            token = r.json().get('token') or r.json().get('access') or r.json().get('refresh')
            # prefer access
            if isinstance(token, dict):
                token = token.get('access')
            # decode user id
            uid = None
            try:
                decoded = jwt.decode(token, options={"verify_signature": False})
                uid = decoded.get('user_id') or decoded.get('user') or decoded.get('id')
            except Exception:
                pass
            # fetch profile
            profile = None
            if uid:
                pr = requests.get(f"{BASE}/api/users/{uid}/profile/", headers={'Authorization': f'Bearer {token}'}, timeout=10)
                profile = {'status': pr.status_code, 'data': pr.json() if pr.status_code==200 else pr.text}
            # fetch projects list
            pj = requests.get(f"{BASE}/api/projects/", timeout=10)
            pj_list = {'status': pj.status_code, 'count': len(pj.json()) if pj.status_code==200 else None}

            results.append({'username': username, 'email': email, 'login': True, 'uid': uid, 'profile': profile, 'projects': pj_list})
        else:
            results.append({'username': username, 'email': email, 'login': False, 'resp': r.text, 'status': r.status_code})
    except Exception as e:
        results.append({'username': username, 'email': email, 'error': str(e)})

print(json.dumps(results, indent=2))
