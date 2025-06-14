import requests
import json


def send_request(api_id):
    url = "http://localhost:4566/restapis/" + api_id + "/dev/_user_request_/roles"
    data = {
        "action": "put",
        "id": "1",
        "type": "admin",
        "permissions": {"read": True, "write": True}
    }

    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
    print(response.status_code)
    print(f"Status code: {response.status_code}")
    print(f"Response text: {response.text}")
    try:
        print(response.json())
    except Exception:
        print("There is no JSON in answer")
