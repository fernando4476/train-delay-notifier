import os

from fastapi import FastAPI
from fetch_train_info import fetch_train_info, find_delays
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

token = os.getenv("ODPT_TOKEN")

@app.get("/delays")
def get_delay():
    delays = find_delays(fetch_train_info(token))
    return delays
