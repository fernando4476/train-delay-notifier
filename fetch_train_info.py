import os
import sys

import requests
from dotenv import load_dotenv

URL = "https://api.odpt.org/api/v4/odpt:TrainInformation"

STATUS_TRANSLATIONS = {
    "遅延": "Delay",
    "運転見合わせ": "Service suspended",
    "ダイヤ乱れ": "Schedule disrupted",
    "運転再開": "Service resumed",
    "運休": "Cancelled",
}


def fetch_train_info(token):
    response = requests.get(URL, params={"acl:consumerKey": token}, timeout=10)
    response.raise_for_status()
    return response.json()


def parse_line(item):
    line_name = item["odpt:railway"].split(".")[-1]
    disrupted = "odpt:trainInformationStatus" in item

    if disrupted:
        train_status = item["odpt:trainInformationStatus"]
        status_ja = train_status.get("ja")
        status_label = train_status.get("en") or STATUS_TRANSLATIONS.get(status_ja, status_ja)
    else:
        status_label = "Normal service"

    texts = item["odpt:trainInformationText"]
    status_text = texts.get("en") or texts.get("ja")

    return {
        "line": line_name,
        "disrupted": disrupted,
        "status": status_label,
        "message": status_text,
    }


def parse_lines(train_info):
    parsed_lines = []
    for entry in train_info:
        parsed_lines.append(parse_line(entry))
    return parsed_lines


def find_delays(train_info):
    delayed = []
    for line in parse_lines(train_info):
        if line["disrupted"]:
            delayed.append(line)
    return delayed


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("ODPT_TOKEN")

    if token is None:
        print("ODPT_TOKEN not found in .env")
        sys.exit()

    try:
        train_info = fetch_train_info(token)
        delays = find_delays(train_info)

        if not delays:
            print("All lines running normally.")
        else:
            for d in delays:
                print("Delayed:", d["line"], "[" + d["status"] + "]", "-", d["message"])

    except requests.exceptions.RequestException as e:
        print("Couldn't reach ODPT:", e)