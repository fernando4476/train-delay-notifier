import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("ODPT_TOKEN")

if token is None:
    print("ODPT_TOKEN not found in .env")
    sys.exit()
else:
    print("Token loaded, length:", len(token))

url = "https://api.odpt.org/api/v4/odpt:TrainInformation"

try:
    response = requests.get(url, params={"acl:consumerKey": token}, timeout=10)
    print("Status:", response.status_code)

    train_info = response.json()
    print("Entries:", len(train_info))
    print(train_info[0])
except requests.exceptions.RequestException as e:
    print("Couldn't reach ODPT:", e)