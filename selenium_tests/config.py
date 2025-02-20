import yaml

'''
Currently since this is being pushed to git I have put config.yaml 
which contains credentials as a .gitignore file

When you do a git pull please add a config.yaml file into your folder structure
Below is the structure of config.yaml file
credentials:
  username: "your_username"
  password: "your_password"
url: "your_URL"
'''

def load_config():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

config = load_config()
USERNAME = config["credentials"]["username"]
PASSWORD = config["credentials"]["password"]
URL = config["url"]
