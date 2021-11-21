import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
rapidkey = os.environ.get("RAPIDKEY")

async def getAnime(message):

  url = "https://jikan1.p.rapidapi.com/search/anime"

  querystring = {"q":message}

  headers = {
    'x-rapidapi-host': "jikan1.p.rapidapi.com",
    'x-rapidapi-key': rapidkey
  }

  response = json.loads(requests.get(url, headers=headers, params=querystring).content)
  
  returnlist = [response["results"][0]["url"], response["results"][0]["image_url"]]

  return returnlist