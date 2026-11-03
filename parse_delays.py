import json

with open("sample_train_info.json") as f:
    train_info = json.load(f)
    print(len(train_info))

for item in train_info:
    if "odpt:trainInformationStatus" in item:
                print("Delayed:", item["odpt:railway"], "-",
                    item["odpt:trainInformationText"]["en"])

