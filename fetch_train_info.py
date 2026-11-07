import os
import sys
import requests

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("ODPT_TOKEN")
response = requests.get("https://api.odpt.org/api/v4/odpt:TrainInformation", params={"param_name": token}, timeout=10)


if token is None:
    print("ODPT_TOKEN not found in .env")
    sys.exit()
else:
    print("Token loaded, length:", len(token))