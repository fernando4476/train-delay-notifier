import os

import requests
from fastapi import FastAPI, HTTPException
from fetch_train_info import fetch_train_info, find_delays, parse_lines
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

token = os.getenv("ODPT_TOKEN")


@app.get("/delays")
def get_delays():
    try:
        delays = find_delays(fetch_train_info(token))
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Service Unavailable: Unable to fetch train information.")
    return delays


@app.get("/lines")
def get_lines():
    try:
        lines = parse_lines(fetch_train_info(token))
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Service Unavailable: Unable to fetch train information.")
    return lines