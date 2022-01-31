#Stone Free - Discord bot dedicated to Jolyne Meme Discord server
#Main developer is Fabucik#9160 on Discord

import os
import discord
import requests
import json
from facts import createFact, getFact, getSpecificFact
from giveaway import chooseWinner
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
import time
import random
import define
import currency
from anime import getAnime
from insult import inSult

load_dotenv()

APIKEY = os.environ.get('APIKEY')
TOKEN = os.environ.get('TOKEN')

caturl = "https://cataas.com/cat?json=true"
facturl = "https://uselessfacts.jsph.pl/random.json?language=en"
jokeurl = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"

intent = discord.Intents.default()
intent.members = True

bot = discord.Client(intents=intent, activity=discord.Game("with your mom"))

commands = """
~jgif: returns random jojo gif
~cimg: returns random cat image
~cgif: returns random cat gif
~addfact <username> <fact>: adds fact about staff member to the database
~fact <username>: returns fact about the staff member
~randomfact: returns fact about random staff member
~giveaway <role id>: chooses random user that is also member of the role id argument
~acd: returns most active chat in the last 10 minutes
~stand: returns random stand and stand stats from anime
~exchange <from> <to> <amount>: exchanges currencies
~afk <afk message>: sets your AFK (only for mods)
~anime <name>: returns image of anime and MyAnimeList URL)
~hotlines: returns international suicide hotlines
~say <message to say>: say thing (only works for staff members)
~insult <person to insult>: insults person lol
"""

@bot.event
async def on_ready():
  print("logged in")
  loopTask.start()
  #pingRole.start()
  #uselessFact.start()


@bot.event
async def on_message(message):
  if message.author == bot.user and "<@&818625208902352898>" not in message.content:
    return
  
  if message.channel.id == 818864719217295400:
    global mestime
    mestime = time.time()
    
  if "<@&818625208902352898>" in message.content:
    global revtime
    revtime = time.time()
  
  #HELP#
  #HELP#
  if message.content.startswith("~help"):
    await message.channel.send(commands)

  #JOJOGIF#
  #JOJOGIF#
  if message.content.startswith("~jgif"):
    getgif = requests.get("https://g.tenor.com/v1/random?key={0}&q=jjba".format(APIKEY))
    gif = getgif.json()["results"][0]["url"]
    await message.channel.send(gif) 


  #CATIMG#
  #CATIMG#
  if message.content.startswith("~cimg"):
    getcat = requests.get(caturl)
    jsoncat = json.loads(getcat.content)
    cat = jsoncat["url"]
    await message.channel.send("https://cataas.com{0}".format(cat))

  #CATGIF#
  #CATGIF#
  if message.content.startswith("~cgif"):
    getcgif = requests.get("https://g.tenor.com/v1/random?key={0}&q=cat".format(APIKEY))
    catgif = getcgif.json()["results"][0]["url"]
    await message.channel.send(catgif)

  #MODFACTS#
  #MODFACTS#
  if message.content.startswith("~addfact"):
    if message.author.guild_permissions.ban_members:
      try:
        createFact(message)
        await message.channel.send("Succesfully added fact")
      except Exception as e:
        await message.channel.send(e)

  if message.content.startswith("~randomfact"):
    try:
      fact = getFact()
      await message.channel.send(fact)
    except Exception as e:
      await message.channel.send(e)

  if message.content.startswith("~fact"):
    try:
      fact = getSpecificFact(message)
      await message.channel.send(fact)
    except Exception as e:
      await message.channel.send(e)

  #GIVEAWAY#
  #GIVEAWAY#
  if message.content.startswith("~giveaway"):
    for member in message.channel.guild.members:
      if member.guild_permissions.ban_members and member.id == message.author.id:
        try:
          await chooseWinner(message)
        except Exception as e:
          await message.channel.send(e)
  

  #ACTIVITY DETECTOR#
  #ACTIVITY DETECTOR#
  with open("channels.json", "r+") as file:
    try:
      data = json.load(file)
    except:
      pass
  try:
    with open("channels.json", "w") as wfile:
      for i in range(len(data["channels"])):
        key = data["channels"][i].keys()
        for j in key:
          if int(j) == message.channel.id:
            for n in data["channels"][i].keys():
              data["channels"][i][n] += 1
              json.dump(data, wfile, indent=2)


      if message.content.startswith("~acd"):
        valuelist = []
        for m in range(len(data["channels"])):
          values = data["channels"][m].values()
          for v in values:
            valuelist.append(v)
            
        valcheck = 0

        for h in range(len(data["channels"])):
          maxvalue = max(valuelist)
          valcheck += 1
          for v in data["channels"][h].values():
            if v == maxvalue:
              for k in data["channels"][h].keys():
                await message.channel.send("<#{0}> is the most active channel in the past 10 minutes".format(int(k)))

  except:
    pass
  
  
  #JOKE#
  #JOKE#
  if message.content.startswith("~joke"):
    jokecontent = requests.get(jokeurl).content.decode("utf-8")
    joke = json.loads(jokecontent)["joke"]
    await message.channel.send(joke)
    
  
  
  #STAND#
  #STAND#
  if message.content.startswith("~stand"):
    try:
      with open("stands.json", "r") as standfile:
        stands = json.load(standfile)
        
        partlist = []
        for i in stands:
          partlist.append(i)
          
        idx = random.choice(partlist)
        partdict = stands[idx]
        
        standlist = []
        for k in partdict:
          standlist.append(k)
          
        standdict = random.choice(standlist)
        
        standparams = [] 
        for j in standdict.keys():
          if j == "stand_type":
            pass
              
          else:
            standparams.append(j)
        
        finalstandlist = []
        for s in standparams:
          if s == "stand_image":
            forms = "Stand Image"
          
          elif s == "user_image":
            forms = "User Image"
            
          elif s == "user":
            forms = "User"
            
          elif s == "Stand":
            forms = "Stand"
            
          elif s == "gender":
            forms = "Gender"
            
          elif s == "hair_color":
            forms = "Hair Color"
            
          elif s == "eye_color":
            forms = "Eye Color"
            
          finalstandlist.append("{0}: {1}".format(forms, standdict[s]))
        
        stand = ", \n".join(finalstandlist)
        standtype = []
        standtype.append("Stand Type: {0}".format(standdict["stand_type"]))
        stand.join(standtype)
        
        await message.channel.send(stand)

    except Exception as e:
      print(e)

  if message.content.startswith("~hotlines"):
    await message.channel.send("If anyone is contemplating suicide, don't do it. There is a lot of people that care about you and it's just not worth it. If you need further help, this is the american suicide prevention hotline: 1-800-273-8255. Here are other ones: https://media.discordapp.net/attachments/898520777358446632/899023898467782666/image0.jpg")
    
    
  #DEFINE#
  #DEFINE#
  #if message.content.startswith("~define"):
  # try:
  #   mes = message.content.split("~define ", 1)[1]
  #   definition = define.define(mes)
  #   await message.channel.send(definition)
  # except Exception as e:
  #   print(e)
      
  #if message.content.startswith("~define fabucik") or message.content.startswith("~define Fabucik"):
  # try:
  #   await message.channel.send("The creator of this bot aka Stone Free")
      
  # except Exception as e:
  #   print(e)
      
      
  #EXCHANGE#
  #EXCHANGE#
  if message.content.startswith("~exchange"):
    try:
      mes = message.content.split(" ", 3)
      frm = mes[1]
      to = mes[2]
      hwmuch = mes[3]
      exchange = currency.exchange(frm, to, hwmuch)
      await message.channel.send("{0} {1} is {2} {3}".format(hwmuch, frm, to, exchange))
      
    except Exception as e:
      print(e)
   
  #PERSONALAFK#
  #PERSONALAFK#
  try:
    for member in message.channel.guild.members:
      if member.guild_permissions.ban_members and member.id == message.author.id:
        if message.content.startswith("~afk"):
          try:
            afk = message.content.split("~afk ", 1)[1]
          except:
            afk = "Not specified"
          try:
            with open("afk.json", "r") as rf:
                data = json.load(rf)
                
          except:
            data = {}
            data["users"] = []
            
          with open("afk.json", "w") as afkfile:
            try:
              for us in range(len(data["users"])):
                for i in data["users"][us].values():
                  if i == message.author.id:
                    data["users"].pop(us)
                    
            except:
              pass

            data["users"].append({"user": message.author.id, "afk": afk, "afkbool": True, "afktime": time.time()})
            json.dump(data, afkfile, indent=2)
          
          user = bot.get_user(message.author.id)
          await message.channel.send("{0}, i set your AFK to: {1}".format(user.name, afk))
          
  except Exception as e:
    print(e)
     
  try:
    with open("afk.json", "r") as f:
      data = json.load(f)
      for u in range(len(data["users"])):
        for key in data["users"][u].keys():
          if key == "user":
            userid = int(data["users"][u]["user"])
            user = bot.get_user(userid)
            if user.mentioned_in(message):
              if data["users"][u]["afkbool"] == True:
                await message.channel.send("{0} is currently afk: {1}".format(user.name, data["users"][u]["afk"]))
    
    for u in range(len(data["users"])):
      if message.author.id == int(data["users"][u]["user"]):
        if data["users"][u]["afkbool"] == True:
          if (time.time() - int(data["users"][len(data["users"])-1]["afktime"])) >= 30:
            await message.channel.send("Welcome back <@{0}> <3".format(message.author.id))
            with open("afk.json", "w") as wf:
              data["users"][u]["afkbool"] = False
              json.dump(data, wf, indent=2)
            break
          
  except Exception as e:
    print(e)
    
  
  #GETANIME#
  #GETANIME#
  try:
    if message.content.startswith("~anime"):
      anime = message.content.split("~anime ", 1)[1]
      alist = await getAnime(anime)
      mes = "\n".join(alist)
      await message.channel.send(mes)
  except Exception as e:
    print(e)
  
  
  #SAY#
  #SAY#
  if message.content.startswith("~say"):
    for member in message.channel.guild.members:
      if member.id == message.author.id:
        if member.guild_permissions.ban_members:
          try:
            mes = message.content.split("~say ", 1)[1]
            if message.reference != None:
              channel = bot.get_channel(message.reference.channel_id)
              msg = await channel.fetch_message(message.reference.message_id)
              await msg.reply(mes, mention_author=True)
              await message.delete()
              print("done")
            else:
              await message.channel.send(mes)
              await message.delete()
            
          except Exception as e:
            print(e)

  #INSULT#
  #INSULT#
  if message.content.startswith("~insult"):
    try:
      inslt = inSult()
      await message.channel.send(f"{inslt} <@{message.author.id}>")
    except Exception as err:
      print(err)

#USELESSFACT#
#USELESSFACT#
@tasks.loop(minutes=15)
async def uselessFact():
  try:
    channel = bot.get_channel(818864719217295400)
    factcontent = requests.get(facturl).content.decode("utf-8")
    fact = json.loads(factcontent)["text"]
    await channel.send(fact)
  except Exception as e:
    print(e)
    
@tasks.loop(minutes = 10)
async def loopTask():
  with open("channels.json", "w") as file:
    data = {}
    data["channels"] = []
    channels = []
    serverid = 788975395486957579
    server = bot.get_guild(serverid)
    for channel in server.channels:
      if str(channel.type) == "text":
         channels.append(channel.id)
          
    for j in channels:
      data["channels"].append({j: 0})

    json.dump(data, file, indent=2)

bot.run(TOKEN)
