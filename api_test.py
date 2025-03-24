import requests

BASE_URL = "http://127.0.0.1:5000"  

def test_register_user():
    url = f"{BASE_URL}/register"
    payload = {"email": "testuser@example.com", "password": "password123"}
    response = requests.post(url, json=payload)
    assert response.status_code in [201, 400]  

def test_register_missing_email():
    url = f"{BASE_URL}/register"
    payload = {"email": "", "password": "password123"}
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert response.json()['error'] == 'Email and password are required'

def test_register_user_exists():
    # First, register the user
    url = f"{BASE_URL}/register"
    payload = {"email": "duplicateuser@example.com", "password": "password123"}
    response = requests.post(url, json=payload)
    assert response.status_code == 201

    # Now, try to register again with the same email
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert response.json()['error'] == 'User already exists'

def test_login():
    url = f"{BASE_URL}/login"
    payload = {"email": "testuser@example.com", "password": "password123"}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_login_invalid_credentials():
    url = f"{BASE_URL}/login"
    payload = {"email": "testuser@example.com", "password": "wrongpassword"}
    response = requests.post(url, json=payload)
    assert response.status_code == 401
    assert response.json()['error'] == 'Invalid credentials'

def test_get_quiz_questions():
    url = f"{BASE_URL}/quiz"
    response = requests.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_submit_quiz():
    url = f"{BASE_URL}/submit_quiz"
    payload = {"user_id": 1, "answers": {"1": 2}}  # Example question ID and answer
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "score" in response.json()

if __name__ == "__main__":
    test_register_user()
    test_login()
    test_get_quiz_questions()
    test_submit_quiz()
    test_register_missing_email()
    test_register_user_exists()
    test_login_invalid_credentials()
