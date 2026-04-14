import urllib.request
import urllib.error
import json
import random
import time

BASE_URL = "http://localhost:8000/api/v1"

def authenticate_simulator():
    """Registers if necessary, and logs in to get a token."""
    username = "simulator_bot"
    password = "SecurePassword123!"
    
    # Try to register
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=json.dumps({"username": username, "email": "sim@bot.com", "password": password}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req)
        print("Simulator registered.")
    except urllib.error.HTTPError as e:
        # 400 likely means user already exists
        if e.code != 400:
            print(f"Registration err: {e.code}")

    # Login
    req = urllib.request.Request(
        f"{BASE_URL}/auth/login",
        data=json.dumps({"username": username, "password": password}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        return data["access_token"]

def start_simulation(token):
    print("Starting transaction simulation...")
    locations = ["New York, US", "London, UK", "Tokyo, JP", "Berlin, DE", "Online", "San Francisco, US", "Unknown", "Moscow, RU"]
    
    while True:
        # Determine if suspicious (10% chance)
        is_suspicious = random.random() < 0.10
        
        amount = round(random.uniform(5000, 15000), 2) if is_suspicious else round(random.uniform(5, 400), 2)
        tx_type = "debit" if random.random() < 0.8 else "credit"
        location = random.choice(locations)
        if is_suspicious and random.random() < 0.5:
            location = "Anonymous Proxy"

        tx_payload = {
            "amount": amount,
            "transaction_type": tx_type,
            "location": location
        }

        req = urllib.request.Request(
            f"{BASE_URL}/transactions/",
            data=json.dumps(tx_payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        try:
            with urllib.request.urlopen(req) as res:
                res_data = json.loads(res.read().decode())
                print(f"Inserted TX: ${res_data['amount']} ({res_data['status']}) at {res_data['location']}")
        except urllib.error.HTTPError as e:
            print("Failed to insert transaction:", e.read().decode())

        # Sleep between 1 and 4 seconds
        time.sleep(random.uniform(1.0, 4.0))

if __name__ == "__main__":
    time.sleep(2)  # Give server time in case it just restarted
    try:
        token = authenticate_simulator()
        start_simulation(token)
    except Exception as e:
        print("Simulation failed:", e)
