import json

with open('config.json', 'r') as file:
    config = json.load(file)

asst_id = config.get("assistant_id")
open_api_key = config.get('open_api_key')
app_secret = config.get("app_secret")