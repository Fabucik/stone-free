import requests
import json

from dotenv import load_dotenv
import os

load_dotenv()
rapidkey = os.environ.get("RAPIDKEY")

def define(message):
  url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

  querystring = {"term": message}

  headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': rapidkey
  }

  response = json.loads(requests.get(url, headers=headers, params=querystring).content)
  
  return response["list"][0]["definition"]