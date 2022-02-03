import json
import random


def createFact(message):
  mes = message.content.split("~addfact ", 1)
  userafact = mes[1].split(' "', 1) or mes[1].split(' ”', 1)
  print(userafact)
  fact = userafact[1].split('"', 1)[0]
  print(fact)
  user = userafact[0]
  print("yes")
  with open("facts.json", "r") as rfile:
    data = json.load(rfile)
      
  with open("facts.json", "w") as wfile:
    data[user] = fact
    json.dump(data, wfile, indent=2)

def getFact():
  with open("facts.json", "r") as rfile:
    data = json.load(rfile)
  user = random.choice(list(data.keys()))
  fakt = data[user]
  return fakt
  
def getSpecificFact(message):
  with open("facts.json", "r") as rfile:
    data = json.load(rfile)
  user = message.content.split("~fact ", 1)[1]
  keys = data.keys()
  if user in keys:
    print(data[user])
    return data[user]