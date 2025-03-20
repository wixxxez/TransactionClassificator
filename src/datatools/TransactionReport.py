import pandas as pd
import time
from datetime import datetime

class Dataset():

    def __init__(self, config:dict):
        
        self.config = config['data_info']

    
    def create_dataset(self) -> pd.DataFrame:

        """Return dataset created used config path"""

        self.data = pd.read_csv(self.config['transaction_path'])
        self.mcc = pd.read_csv(self.config['mcc_code_path'])
        self.Balances = pd.read_csv(self.config['balances_table_path']) 

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

    def get_balances(self): 

        return self.Balances

class OverallTransactionReport():

    def __init__(self, dataset: pd.DataFrame, balance: pd.DataFrame):
        self.dataset = dataset
        self.balance = balance

    def get_transaction_report(self) -> pd.DataFrame: 

        today = datetime.today()
        current_week = today.isocalendar()[1]
 
        dataset = self.dataset.query("week_number == @current_week").groupby( ['user_name', 'custom_category'] ).amount.sum().to_frame()

        if len(dataset) == 0: 
 
            raise RuntimeError("No transactions for current week.")
        
        dataset = dataset.reset_index().rename(columns={'custom_category':'category'})
        return dataset
    
    def get_markdown_response(self) : 

         
        today = datetime.today()
        current_week = today.isocalendar()[1]
 
        dataset = self.dataset.query("week_number == @current_week").groupby( ['user_name', 'custom_category'] ).amount.sum().to_frame()

        if len(dataset) == 0: 

            return "No transactions for current week."
        
        return dataset.to_markdown()
    
    def get_Weekly_balance_report(self, markdown = True): 

        data_full = self.dataset
        Balances = self.balance

        Weekly = data_full.query("week_number == 1").groupby( ['custom_category'] ).amount.sum().reset_index().merge(Balances.query('Period == "w"'),how='right')
        Weekly = Weekly.fillna(0)
        balance_report_body_list = []
        for category in Weekly.custom_category.unique():

            category_df = Weekly.query("custom_category == @category")

            availible = category_df['Balance'] -category_df['amount']
            availible = availible[0]
            if availible > 0 : 
                balance_report_body = f"For category {category}. You have {availible}. UAH"

            else :
                balance_report_body = f"For category {category}. You exceeded the weekly limit."

            balance_report_body_list.append(balance_report_body)
        
        if markdown:
            return Weekly.to_markdown(), balance_report_body_list
        
        else : return Weekly, balance_report_body_list
    
    def get_month_balance_report(self, markdown = True): 
        data_full = self.dataset
        Balances = self.balance
        today = datetime.today()
        current_month = today.month

        Monthly = data_full.query("month_number == @current_month").groupby( ['custom_category'] ).amount.sum().reset_index().merge(Balances.query('Period == "m"'),how='right')
        Monthly = Monthly.fillna(0)

        balance_report_body_list = []
        for category in Monthly.custom_category.unique():

            category_df = Monthly.query("custom_category == @category")

            availible = category_df['Balance'] -category_df['amount']
            availible = availible.reset_index()[0][0]
            if availible > 0 : 
                balance_report_body = f"For category {category}. You have {availible} UAH."

            else :
                balance_report_body = f"For category {category}. You exceeded the monthly limit."
            balance_report_body_list.append(balance_report_body)

        if markdown :
            return Monthly.to_markdown(), balance_report_body_list

        else: return Monthly, balance_report_body_list

    
