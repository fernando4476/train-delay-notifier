import requests

url = "https://tetsudo.rti-giken.jp/free/delay.json"

try:
    response = requests.get(url,timeout = 10)
    print(response.status_code)
    print(response.json())
except requests.exceptions.RequestException as e:
    print("Couldn't reach the delay feed:", e)




