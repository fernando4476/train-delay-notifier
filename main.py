import os

from fastapi import FastAPI
from fetch_train_info import fetch_train_info, find_delays, parse_lines
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

token = os.getenv("ODPT_TOKEN")


@app.get("/delays")
def get_delays():
    delays = find_delays(fetch_train_info(token))
    return delays


@app.get("/lines")
def get_lines():
    lines = parse_lines(fetch_train_info(token))
    return lines