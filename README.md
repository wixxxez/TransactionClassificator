## Transaction classificator. 
Main goal to classify transaction from bank account to custom categories. 

### Data Acquisition step 

- Monobank transaction history from last month. (31 day + one hour)
    
    1.  Get your personall api token from: https://api.monobank.ua/index.html

    2. Setup it as environment variable 

            set MONO_TOKEN = 'your_token'

    3. Run the script 


            python MonoDataAquisitionRequestJob.py

    4. The uploaded data will be saved in the data directory as **.json** file

