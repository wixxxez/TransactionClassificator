import requests
import os
import requests
import json
import time
import datetime
s = "26/11/2024"
to = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
 
MONOBANK_TOKEN = os.environ['MONO_TOKEN']
print("Timestamp:", int(to))
url = "https://api.monobank.ua/personal/statement/"  # Replace with the actual API endpoint URL

data = {
    "account": "9CMjgVvxC3N2sQzhWHyZwQ",
    "from": int(to) - 2682000 ,
    "to": int(to)
}

url = f"{url}/{data['account']}/{data['from']}/{data['to']}"
headers = {
    "X-Token": MONOBANK_TOKEN
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Request successful")
    print("Amount of collected Transaction is: ", len(response.json()))
    with open('./data/MonobankTransactionHistory.json', 'w') as f:
        json.dump(response.json(), f) # Assuming the response is in JSON format
else:
    print("Request failed with status code:", response.status_code)
    print(response.text)  