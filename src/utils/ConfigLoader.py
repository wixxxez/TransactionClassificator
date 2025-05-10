import yaml
from google.cloud import storage
 


# def load_config(config_path): 
# # Load the YAML file
#     with open(config_path, "r") as file:
#         config = yaml.safe_load(file)

#     return config

def load_config(config_path): 

    client = storage.Client()
    bucket_name, file_name = config_path.split('/')
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()
    
    return yaml.safe_load(content)
     

def LoadUserConfigById(cfg, id): 

    users = cfg['users']
    
    user_info = [i  for i in users if id == i['id'] ]
    return user_info[0]

def LoadAllUsersCFG(cfg):

    return cfg['users']