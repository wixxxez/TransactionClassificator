import time 
import requests
from datetime import datetime
Today = time.strftime('%d/%m/%Y')
to = time.mktime(datetime.strptime(Today, "%d/%m/%Y").timetuple())
        
MONOBANK_TOKEN = 'umy5NlYxv9hiubq1c1fzr-2-zB7NGIXGraucAzgoAADY'
        
url = "https://api.monobank.ua/personal/statement/"  # Replace with the actual API endpoint URL

data = {
            "account": '9CMjgVvxC3N2sQzhWHyZwQ',
            "from": int(to) - 2682000 ,
            "to": int(to)
        }

url = f"{url}/{data['account']}/{data['from']}/{data['to']}"
headers = {
            "X-Token":  MONOBANK_TOKEN
        }

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Request successful")
    print("Amount of collected Transaction is: ", len(response.json()))

    print(response.text)
else:
    print("Request failed with status code:", response.status_code)
    print(response.text)

    raise RuntimeError( f"Request is failed. Status code is: {response.status_code}" ) 
