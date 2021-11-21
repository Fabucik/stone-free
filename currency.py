import requests
import json

from dotenv import load_dotenv
import os

load_dotenv()
rapidkey = os.environ.get("RAPIDKEY")

def exchange(frm, to, hwmuch):

  url = "https://api.frankfurter.app/latest"

  querystring = {"from": frm,"to":to,"amount": hwmuch}

  headers = {
    'x-rapidapi-host': "https://currencyconverter.p.rapidapi.com/",
    'x-rapidapi-key': rapidkey
   }

  response = json.loads(requests.get(url, headers=headers, params=querystring).content)["rates"][to]

  return response