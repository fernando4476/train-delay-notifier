import os
import sys
import requests
from dotenv import load_dotenv

URL = "https://api.odpt.org/api/v4/odpt:TrainInformation"


def fetch_train_info(token):
    response = requests.get(URL, params={"acl:consumerKey": token}, timeout=10)
    return response.json()


def find_delays(train_info):
    delayed_lines = []
    for item in train_info:
        if "odpt:trainInformationStatus" in item:
            line_name = item["odpt:railway"].split(".")[-1]
            train_status = item["odpt:trainInformationStatus"]
            status_label = train_status.get("en") or train_status.get("ja")
            texts = item["odpt:trainInformationText"]
            status_text = texts.get("en") or texts.get("ja")

            delayed_lines.append({
                "line": line_name,
                "status": status_label,
                "message": status_text,
            })
    return delayed_lines

def parse_line(item):
    parse_arr = []
    for item in train_info:
        line_name = item["odpt:railway"].split(".")[-1]
        disrupted = "odpt:trainInformationStatus" in item

        if disrupted:
            train_status = item["odpt:trainInformationStatus"]
            status_label = train_status.get("en") or train_status.get("ja")
        else:
            status_label = "Normal service"

        texts = item["odpt:trainInformationText"]
        status_text = texts.get("en") or texts.get("ja")

        parse_arr.append({
            "line": line_name,
            "disrupted": disrupted,
            "status": status_label,
            "message": status_text,
        })

    return parse_arr




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