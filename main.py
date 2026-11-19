import asyncio
import os
from contextlib import asynccontextmanager

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from db import Base, engine
from fetch_train_info import fetch_train_info, find_delays, parse_lines
from history import record_delays

load_dotenv()
token = os.getenv("ODPT_TOKEN")


def check_once():
    try:
        delays = find_delays(fetch_train_info(token))
        record_delays(delays)
        print("Checked ODPT:", len(delays), "delays")
    except requests.exceptions.RequestException:
        print("Check failed, will retry")


async def poll_forever():
    while True:
        await asyncio.to_thread(check_once)
        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)
    task = asyncio.create_task(poll_forever())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)


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