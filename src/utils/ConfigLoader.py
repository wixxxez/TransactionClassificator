import yaml

 


def load_config(config_path): 
# Load the YAML file
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config

def LoadUserConfigById(cfg, id): 

    users = cfg['users']
    
    user_info = [i  for i in users if id == i['id'] ]
    return user_info[0]