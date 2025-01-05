import requests
import os
import requests
import json
import time
from datetime import datetime
import pandas as pd


class DataAcquisition(): 

    def __init__(self, mono_token, mono_account):
        
        self.mono_token = mono_token
        self.mono_account = mono_account

    def run(self):

        Today = time.strftime('%d/%m/%Y')
        to = time.mktime(datetime.strptime(Today, "%d/%m/%Y").timetuple())
        
        MONOBANK_TOKEN = os.environ['MONO_TOKEN']
        
        url = "https://api.monobank.ua/personal/statement/"  # Replace with the actual API endpoint URL

        data = {
            "account": self.mono_account,
            "from": int(to) - 2682000 ,
            "to": int(to)
        }

        url = f"{url}/{data['account']}/{data['from']}/{data['to']}"
        headers = {
            "X-Token":  self.mono_token
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("Request successful")
            print("Amount of collected Transaction is: ", len(response.json()))
            return response.json() # Assuming the response is in JSON format
        else:
            print("Request failed with status code:", response.status_code)
            print(response.text)

            raise RuntimeError( f"Request is failed. Status code is: {response.status_code}" ) 


class DataPreprocessing():

    def __init__(self, telegram_id, name):

        self.name = name
        self.telegram_id = telegram_id


    def run(self, json_data: list):

        mono_df = pd.DataFrame(json_data)
        mono_df['type'] = mono_df['amount'].apply(lambda x:  'income' if int(x) > 0 else 'outcome')
        mono_df['amount'] = mono_df['amount'].apply(lambda x:  abs(int(str(x)[:-2])) )
        mono_df['full_date'] = mono_df['time'].apply( lambda x : datetime.fromtimestamp(x).strftime("%d.%m.%Y")) 
        mono_df["month_number"] =  mono_df['time'].apply( lambda x : datetime.fromtimestamp(x).month) 
        mono_df["week_number"] = mono_df['time'].apply( lambda x : datetime.fromtimestamp(x).isocalendar()[1]) 
        mono_df = mono_df[['id','time','description','originalMcc', 'amount','receiptId','type','full_date','month_number','week_number']]
        mono_df['full_date'] = mono_df['full_date'].apply(lambda x: x.replace('.','-'))
        # mono_df['full_date']  = pd.to_datetime(mono_df['full_date'])
        mono_df['user_name'] = self.name
        mono_df['telegram_id'] = self.telegram_id

        return mono_df

def save_data(data: pd.DataFrame):

    old_data = pd.read_csv("./datasets/transaction_history.csv", index_col=0) 

    pd.concat([old_data, data]).drop_duplicates('id').to_csv("./datasets/transaction_history.csv")
class DataAcquisitionPipeline():

    def __init__(self, id, name, monobank_token, monobank_account): 

        self.telegram_id = id
        self.name = name
        self.mono_token = monobank_token
        self.mono_acc = monobank_account

        
    
    def run(self):

        data_acq = DataAcquisition(self.mono_token, self.mono_acc)

        data = data_acq.run()
        
        processing_pipe = DataPreprocessing(self.telegram_id,self.name)
        preprocessed_data = processing_pipe.run(data)
        save_data(preprocessed_data)
        
         

    