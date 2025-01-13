import pandas as pd
import time

class Dataset():

    def __init__(self, config:dict):
        
        self.config = config['data_info']

    
    def create_dataset(self) -> pd.DataFrame:

        """Return dataset created used config path"""

        self.data = pd.read_csv(self.config['transaction_path'])
        self.mcc = pd.read_csv(self.config['mcc_code_path'])
        self.Balances = pd.read_csv(self.config['balance_table_path']) 

        custom_categories = {
                    'MCC_Categories' :  [{'originalMcc' : '5812', 'custom_category': 'Харчування'},{'originalMcc' : '5499', 'custom_category': 'Харчування'},{'originalMcc' : '5411', 'custom_category': 'Харчування'}],
                    'Description_Categories' : [{'description' : 'Петро С.', 'custom_category': 'Квартплата'} , {'description': '535129****2010', 'custom_category': 'Комунальний платіж'}]
                    }
        self.data = self.data.merge(self.mcc , on = 'originalMcc')
        mcc_categories = pd.DataFrame([category for category in custom_categories['MCC_Categories']])
        mcc_categories['originalMcc'] = mcc_categories['originalMcc'].astype(int)
        data_with_mcc_categories = self.data.merge(mcc_categories,on='originalMcc', how='left')
        description_categories = pd.DataFrame([category for category in custom_categories['Description_Categories']])
        data_full = data_with_mcc_categories.merge(description_categories, on='description', how='left')
        data_full['custom_category_x']=  data_full['custom_category_x'].fillna(data_full['custom_category_y'])
        data_full['custom_category_x']=  data_full['custom_category_x'].fillna(data_full['Business group'])
        data_full  = data_full.rename(columns={'custom_category_x':'custom_category'})
        del data_full['custom_category_y']
        
        self.dataset = data_full
        return self.dataset


class OverallTransactionReport():

    def __init__(self, dataset: pd.DataFrame, balance: pd.DataFrame):
        self.dataset = dataset
        self.balance = balance

    def get_markdown_response(self) : 

        current_week = int(time.strftime('%w'))
        dataset = self.dataset.query("week_number == @current_week").groupby( ['user_name', 'Business group', 'custom_category'] ).amount.sum().to_frame()

        if len(dataset) == 0: 

            return "No transaction for current week."
        
        return dataset.to_markdown()
    
    def get_Weekly_balance_report(self) : 


        return 0
    
