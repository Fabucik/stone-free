import requests
import json

def inSult():
    url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"

    response = json.loads(requests.get(url).content)["insult"]

    print(response)

    return response